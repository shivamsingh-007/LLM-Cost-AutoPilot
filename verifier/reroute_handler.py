from __future__ import annotations

from typing import Any, Dict, Optional

from core.models_config import ALL_MODELS, ModelConfig
from core.unified_interface import UnifiedLLMInterface


def _pick_highest_tier_model() -> ModelConfig:
    return max(ALL_MODELS, key=lambda m: m.quality_tier)


async def auto_escalate_and_rerun(
    prompt: str,
    routing_metadata: Dict[str, Any],
    llm: Optional[UnifiedLLMInterface] = None,
    logger: Any = None,
):
    llm = llm or UnifiedLLMInterface()
    highest = _pick_highest_tier_model()

    resp = await llm.send_request(
        prompt=prompt,
        model_config=highest,
        system_prompt="You are an authoritative assistant. Provide the best answer.",
        temperature=0.0,
        max_tokens=routing_metadata.get("tokens_out_estimate", 1024),
    )

    if logger:
        logger.log_rerun(
            original_model=routing_metadata.get("model"),
            escalated_model=highest.model_id,
            escalated_response=resp.output,
        )

    return resp
