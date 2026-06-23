from __future__ import annotations

import asyncio
import json
from typing import Any, Callable, Dict, Optional, Tuple

from verifier.classifier_feedback import record_routing_failure
from verifier.judge_prompts import agreement_judge_prompt
from verifier.langfuse_logger import LangfuseLogger
from verifier.reroute_handler import _pick_highest_tier_model


class VerifierPipeline:
    AGREEMENT_THRESHOLD = 0.8

    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._logger = LangfuseLogger()

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

        if agreement < self.AGREEMENT_THRESHOLD:
            failure = {
                "prompt": prompt,
                "agreement": agreement,
                "candidate_model": metadata.get("model"),
                "oracle_model": oracle_model,
            }
            await self._record_failure(failure)

    async def _run_oracle(self, prompt: str) -> Tuple[str, str]:
        return ("", "")

    async def _run_judge(self, prompt: str, candidate: str, oracle: str) -> Tuple[float, str]:
        return (1.0, "mock")

    async def _record_failure(self, failure: Dict[str, Any]):
        record_routing_failure(failure)

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()
