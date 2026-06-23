from __future__ import annotations

import asyncio
import hashlib
import time
from typing import Any, Dict, Optional, Tuple

from storage.duckdb_logger import DuckDBLogger, hash_prompt
from verifier.classifier_feedback import record_routing_failure
from verifier.judge_prompts import agreement_judge_prompt
from verifier.langfuse_logger import LangfuseLogger
from verifier.reroute_handler import _pick_highest_tier_model


class VerifierPipeline:
    AGREEMENT_THRESHOLD = 0.8

    def __init__(self, db_logger: Optional[DuckDBLogger] = None):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._logger = LangfuseLogger()
        self._db_logger = db_logger or DuckDBLogger(":memory:")

    async def enqueue(self, prompt: str, response_text: str, metadata: Dict[str, Any]):
        job = {
            "prompt": prompt,
            "response_text": response_text,
            "metadata": metadata,
        }
        await self._queue.put(job)

    async def process_next(self):
        job = await self._queue.get()
        try:
            await self._process(job)
        finally:
            self._queue.task_done()

    async def _process(self, job: Dict[str, Any]):
        prompt = job["prompt"]
        candidate = job["response_text"]
        metadata = job["metadata"]

        oracle_text, oracle_model = await self._run_oracle(prompt)

        agreement, notes = await self._run_judge(prompt, candidate, oracle_text)

        self._logger.log_verification(
            prompt=prompt,
            candidate_response=candidate,
            oracle_response=oracle_text,
            agreement=agreement,
            notes=notes,
            routing_metadata=metadata,
        )

        escalation = agreement < self.AGREEMENT_THRESHOLD
        if escalation:
            failure = {
                "prompt": prompt,
                "agreement": agreement,
                "candidate_model": metadata.get("model"),
                "oracle_model": oracle_model,
            }
            await self._record_failure(failure)

        # Log to DuckDB
        request_id = f"{hash_prompt(prompt)[:12]}-{int(time.time() * 1000)}"
        self._db_logger.log_request(
            request_id=request_id,
            prompt=prompt,
            complexity_tier=str(metadata.get("tier", "?")),
            routed_model=metadata.get("model", "unknown"),
            baseline_model="gpt-4o",
            input_tokens=metadata.get("input_tokens", 0),
            output_tokens=metadata.get("output_tokens", 0),
            cost_usd=metadata.get("cost_usd", 0.0),
            latency_ms=metadata.get("latency_ms", 0.0),
            quality_score=agreement,
            escalation_flag=escalation,
            success=True,
        )

    async def _run_oracle(self, prompt: str) -> Tuple[str, str]:
        return ("", "")

    async def _run_judge(self, prompt: str, candidate: str, oracle: str) -> Tuple[float, str]:
        return (1.0, "mock")

    async def _record_failure(self, failure: Dict[str, Any]):
        record_routing_failure(failure)

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()
