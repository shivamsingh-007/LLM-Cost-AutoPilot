from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

from models_config import (
    GPT4O, GPT4O_MINI, CLAUDE_HAIKU_4_5, CLAUDE_SONNET_4_6,
    CLAUDE_OPUS_4_6, LLAMA_3_1_8B, LLAMA_3_3_70B,
    ModelConfig, get_model,
)
from unified_interface import UnifiedLLMInterface


class LLMRouter:
    TIER_MODEL_MAP: Dict[str, list[ModelConfig]] = {
        "1": [LLAMA_3_1_8B, GPT4O_MINI, CLAUDE_HAIKU_4_5],
        "2": [GPT4O, LLAMA_3_3_70B, CLAUDE_SONNET_4_6],
        "3": [CLAUDE_OPUS_4_6, CLAUDE_SONNET_4_6, GPT4O],
    }

    def __init__(self):
        self._llm = UnifiedLLMInterface()

    async def route_request(
        self,
        prompt: str,
        context: str = "",
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tier: str = "2",
    ) -> Tuple[str, Dict[str, Any]]:
        models = self.TIER_MODEL_MAP.get(tier, self.TIER_MODEL_MAP["2"])
        last_error = ""

        for model in models:
            resp = await self._llm.send_request(
                prompt=prompt,
                model_config=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if resp.success:
                return resp.output, {
                    "model": model.model_id,
                    "tier": tier,
                    "tokens_input": resp.tokens.get("input", 0),
                    "tokens_output": resp.tokens.get("output", 0),
                    "cost": resp.cost_usd,
                    "latency_ms": resp.latency_ms,
                    "quality_score": 1.0,
                    "success": True,
                }
            last_error = resp.error_message

        return last_error, {"model": models[-1].model_id, "tier": tier, "success": False}
