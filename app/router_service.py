from __future__ import annotations

import time
import uuid
from typing import Dict, Any

from core.router import LLMRouter
from storage.duckdb_logger import DuckDBLogger
from ml.complexity_classifier import ComplexityClassifier


class RoutingService:
    def __init__(self):
        self.router = LLMRouter()
        self.db = DuckDBLogger("data/llm_autopilot.duckdb")
        self.classifier = ComplexityClassifier()
        try:
            self.classifier.load("models/complexity_classifier")
        except Exception:
            self.classifier = None

    def classify_prompt(self, prompt: str) -> Dict[str, Any]:
        if self.classifier:
            pred = self.classifier.predict_complexity(prompt, "")
            return {
                "complexity_tier": pred["tier"],
                "tier_reason": f"classifier={pred['tier']} confidence={pred['confidence']:.2f}",
                "complexity_score": pred["complexity_score"],
            }
        return {
            "complexity_tier": "Tier 2",
            "tier_reason": "fallback heuristic",
            "complexity_score": 0.5,
        }

    async def complete(self, request) -> Dict[str, Any]:
        t0 = time.time()
        request_id = str(uuid.uuid4())

        cls = self.classify_prompt(request.prompt)
        context = ""
        if request.metadata:
            context = request.metadata.get("context", "")

        response, metadata = await self.router.route_request(
            prompt=request.prompt,
            context=context,
            system_prompt=request.system_prompt or "",
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            tier=cls["complexity_tier"],
        )

        latency_ms = (time.time() - t0) * 1000
        quality_score = float(metadata.get("quality_score") or 0.0)
        success = bool(metadata.get("success", True))
        escalation_flag = not success or quality_score < 0.75

        self.db.log_request(
            request_id=request_id,
            prompt=request.prompt,
            complexity_tier=cls["complexity_tier"],
            routed_model=metadata.get("model", ""),
            baseline_model="openai/gpt-4o",
            input_tokens=int(metadata.get("tokens_input", 0)),
            output_tokens=int(metadata.get("tokens_output", 0)),
            cost_usd=float(metadata.get("cost", 0.0)),
            latency_ms=latency_ms,
            quality_score=quality_score,
            escalation_flag=escalation_flag,
            success=success,
        )

        reason = cls["tier_reason"]
        return {
            "output": response,
            "request_id": request_id,
            "model_id": metadata.get("model", ""),
            "routed_model": metadata.get("model", ""),
            "complexity_tier": cls["complexity_tier"],
            "selected_reason": reason,
            "cost_usd": float(metadata.get("cost", 0.0)),
            "latency_ms": latency_ms,
            "quality_score": quality_score,
            "escalation_flag": escalation_flag,
            "success": success,
        }

    def stats(self) -> Dict[str, Any]:
        return self.db.get_summary()
