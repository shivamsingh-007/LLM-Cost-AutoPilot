from __future__ import annotations

import enum
from dataclasses import dataclass, asdict
from typing import Dict, List


class Provider(enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


@dataclass
class ModelConfig:
    provider: Provider
    model_id: str
    display_name: str
    cost_per_input_token: float
    cost_per_output_token: float
    avg_latency_ms: float
    context_window: int
    max_output_tokens: int
    quality_tier: int
    supports_coding: bool = True
    supports_reasoning: bool = True
    supports_multimodal: bool = False
    min_complexity: float = 0.0
    max_complexity: float = 1.0

    def cost_per_token(self, is_output: bool = False) -> float:
        cost = self.cost_per_output_token if is_output else self.cost_per_input_token
        return cost / 1_000_000

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        input_cost = input_tokens * self.cost_per_input_token / 1_000_000
        output_cost = output_tokens * self.cost_per_output_token / 1_000_000
        return input_cost + output_cost

    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "provider": self.provider.value,
        }


GPT4O = ModelConfig(
    provider=Provider.OPENAI,
    model_id="gpt-4o",
    display_name="GPT-4o",
    cost_per_input_token=2.50,
    cost_per_output_token=10.00,
    avg_latency_ms=1500,
    context_window=128_000,
    max_output_tokens=16_384,
    quality_tier=9,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=True,
    min_complexity=0.0,
    max_complexity=1.0,
)

GPT4O_MINI = ModelConfig(
    provider=Provider.OPENAI,
    model_id="gpt-4o-mini",
    display_name="GPT-4o Mini",
    cost_per_input_token=0.15,
    cost_per_output_token=0.60,
    avg_latency_ms=800,
    context_window=128_000,
    max_output_tokens=16_384,
    quality_tier=7,
    supports_coding=True,
    supports_reasoning=False,
    supports_multimodal=True,
    min_complexity=0.0,
    max_complexity=0.6,
)

O1_MINI = ModelConfig(
    provider=Provider.OPENAI,
    model_id="o1-mini",
    display_name="o1-mini",
    cost_per_input_token=3.00,
    cost_per_output_token=12.00,
    avg_latency_ms=3000,
    context_window=128_000,
    max_output_tokens=65_536,
    quality_tier=9,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=False,
    min_complexity=0.3,
    max_complexity=1.0,
)

CLAUDE_3_5_SONNET = ModelConfig(
    provider=Provider.ANTHROPIC,
    model_id="claude-3.5-sonnet",
    display_name="Claude 3.5 Sonnet",
    cost_per_input_token=3.00,
    cost_per_output_token=15.00,
    avg_latency_ms=1800,
    context_window=200_000,
    max_output_tokens=8_192,
    quality_tier=9,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=True,
    min_complexity=0.0,
    max_complexity=1.0,
)

CLAUDE_SONNET_4_6 = ModelConfig(
    provider=Provider.ANTHROPIC,
    model_id="claude-sonnet-4.6",
    display_name="Claude Sonnet 4.6",
    cost_per_input_token=3.00,
    cost_per_output_token=15.00,
    avg_latency_ms=1700,
    context_window=200_000,
    max_output_tokens=8_192,
    quality_tier=10,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=True,
    min_complexity=0.0,
    max_complexity=1.0,
)

CLAUDE_HAIKU_4_5 = ModelConfig(
    provider=Provider.ANTHROPIC,
    model_id="claude-haiku-4.5",
    display_name="Claude Haiku 4.5",
    cost_per_input_token=1.00,
    cost_per_output_token=5.00,
    avg_latency_ms=600,
    context_window=200_000,
    max_output_tokens=8_192,
    quality_tier=6,
    supports_coding=True,
    supports_reasoning=False,
    supports_multimodal=True,
    min_complexity=0.0,
    max_complexity=0.5,
)

CLAUDE_OPUS_4_6 = ModelConfig(
    provider=Provider.ANTHROPIC,
    model_id="claude-opus-4.6",
    display_name="Claude Opus 4.6",
    cost_per_input_token=5.00,
    cost_per_output_token=25.00,
    avg_latency_ms=2200,
    context_window=410_000,
    max_output_tokens=8_192,
    quality_tier=10,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=True,
    min_complexity=0.2,
    max_complexity=1.0,
)

LLAMA_3_3_70B = ModelConfig(
    provider=Provider.OLLAMA,
    model_id="llama3.3-70b",
    display_name="Llama 3.3 70B",
    cost_per_input_token=0.0,
    cost_per_output_token=0.0,
    avg_latency_ms=1200,
    context_window=128_000,
    max_output_tokens=8_192,
    quality_tier=8,
    supports_coding=True,
    supports_reasoning=True,
    supports_multimodal=False,
    min_complexity=0.0,
    max_complexity=0.8,
)

LLAMA_3_1_8B = ModelConfig(
    provider=Provider.OLLAMA,
    model_id="llama3.1-8b",
    display_name="Llama 3.1 8B",
    cost_per_input_token=0.0,
    cost_per_output_token=0.0,
    avg_latency_ms=500,
    context_window=128_000,
    max_output_tokens=8_192,
    quality_tier=5,
    supports_coding=True,
    supports_reasoning=False,
    supports_multimodal=False,
    min_complexity=0.0,
    max_complexity=0.4,
)

ALL_MODELS: List[ModelConfig] = [
    GPT4O,
    GPT4O_MINI,
    O1_MINI,
    CLAUDE_3_5_SONNET,
    CLAUDE_SONNET_4_6,
    CLAUDE_HAIKU_4_5,
    CLAUDE_OPUS_4_6,
    LLAMA_3_3_70B,
    LLAMA_3_1_8B,
]

MODEL_REGISTRY: Dict[str, ModelConfig] = {
    f"{m.provider.value}/{m.model_id}": m for m in ALL_MODELS
}


def get_model(model_id: str) -> ModelConfig:
    model = MODEL_REGISTRY.get(model_id)
    if model is None:
        available = sorted(MODEL_REGISTRY.keys())
        raise ValueError(
            f"Model '{model_id}' not found. Available models: {available}"
        )
    return model


def get_models_by_provider(provider: Provider) -> List[ModelConfig]:
    return [m for m in ALL_MODELS if m.provider == provider]


def get_cheapest_model_for_complexity(complexity: float) -> ModelConfig:
    capable = [
        m for m in ALL_MODELS
        if m.min_complexity <= complexity <= m.max_complexity
    ]
    if not capable:
        return GPT4O
    capable.sort(key=lambda m: (m.cost_per_input_token + m.cost_per_output_token, -m.quality_tier))
    return capable[0]
