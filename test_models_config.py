import pytest

from models_config import (
    Provider,
    ModelConfig,
    MODEL_REGISTRY,
    ALL_MODELS,
    get_model,
    get_models_by_provider,
    get_cheapest_model_for_complexity,
    GPT4O,
    GPT4O_MINI,
    O1_MINI,
    CLAUDE_3_5_SONNET,
    CLAUDE_SONNET_4_6,
    CLAUDE_HAIKU_4_5,
    CLAUDE_OPUS_4_6,
    LLAMA_3_3_70B,
    LLAMA_3_1_8B,
)


class TestProvider:
    def test_enum_values(self):
        assert Provider.OPENAI.value == "openai"
        assert Provider.ANTHROPIC.value == "anthropic"
        assert Provider.OLLAMA.value == "ollama"

    def test_enum_members(self):
        assert len(Provider) == 3


class TestModelConfig:
    def test_dataclass_fields(self):
        cfg = ModelConfig(
            provider=Provider.OPENAI,
            model_id="test-model",
            display_name="Test",
            cost_per_input_token=1.0,
            cost_per_output_token=2.0,
            avg_latency_ms=100,
            context_window=4096,
            max_output_tokens=1024,
            quality_tier=5,
        )
        assert cfg.provider == Provider.OPENAI
        assert cfg.model_id == "test-model"
        assert cfg.supports_coding is True
        assert cfg.supports_reasoning is True
        assert cfg.supports_multimodal is False
        assert cfg.min_complexity == 0.0
        assert cfg.max_complexity == 1.0

    def test_cost_per_token(self):
        c = ModelConfig(
            provider=Provider.OPENAI, model_id="t", display_name="t",
            cost_per_input_token=1.0, cost_per_output_token=2.0,
            avg_latency_ms=100, context_window=4096, max_output_tokens=1024,
            quality_tier=5,
        )
        assert c.cost_per_token(is_output=False) == 1.0 / 1_000_000
        assert c.cost_per_token(is_output=True) == 2.0 / 1_000_000

    def test_estimate_cost(self):
        c = ModelConfig(
            provider=Provider.OPENAI, model_id="t", display_name="t",
            cost_per_input_token=1.0, cost_per_output_token=2.0,
            avg_latency_ms=100, context_window=4096, max_output_tokens=1024,
            quality_tier=5,
        )
        cost = c.estimate_cost(1_000_000, 500_000)
        assert cost == 1.0 + 1.0

    def test_to_dict(self):
        d = GPT4O.to_dict()
        assert d["provider"] == "openai"
        assert d["model_id"] == "gpt-4o"
        assert d["display_name"] == "GPT-4o"
        assert isinstance(d["cost_per_input_token"], float)


class TestModelInstances:
    def test_all_models_present(self):
        assert len(ALL_MODELS) == 9

    def test_gpt4o(self):
        assert GPT4O.provider == Provider.OPENAI
        assert GPT4O.cost_per_input_token == 2.50
        assert GPT4O.cost_per_output_token == 10.00
        assert GPT4O.avg_latency_ms == 1500
        assert GPT4O.context_window == 128_000
        assert GPT4O.quality_tier == 9
        assert GPT4O.supports_multimodal is True

    def test_gpt4o_mini(self):
        assert GPT4O_MINI.provider == Provider.OPENAI
        assert GPT4O_MINI.cost_per_input_token == 0.15
        assert GPT4O_MINI.cost_per_output_token == 0.60
        assert GPT4O_MINI.avg_latency_ms == 800
        assert GPT4O_MINI.quality_tier == 7
        assert GPT4O_MINI.max_complexity == 0.6

    def test_o1_mini(self):
        assert O1_MINI.provider == Provider.OPENAI
        assert O1_MINI.cost_per_input_token == 3.00
        assert O1_MINI.cost_per_output_token == 12.00
        assert O1_MINI.avg_latency_ms == 3000
        assert O1_MINI.max_output_tokens == 65_536
        assert O1_MINI.min_complexity == 0.3

    def test_claude_3_5_sonnet(self):
        assert CLAUDE_3_5_SONNET.provider == Provider.ANTHROPIC
        assert CLAUDE_3_5_SONNET.cost_per_input_token == 3.00
        assert CLAUDE_3_5_SONNET.cost_per_output_token == 15.00
        assert CLAUDE_3_5_SONNET.avg_latency_ms == 1800
        assert CLAUDE_3_5_SONNET.context_window == 200_000
        assert CLAUDE_3_5_SONNET.quality_tier == 9

    def test_claude_sonnet_4_6(self):
        assert CLAUDE_SONNET_4_6.provider == Provider.ANTHROPIC
        assert CLAUDE_SONNET_4_6.cost_per_input_token == 3.00
        assert CLAUDE_SONNET_4_6.cost_per_output_token == 15.00
        assert CLAUDE_SONNET_4_6.avg_latency_ms == 1700
        assert CLAUDE_SONNET_4_6.quality_tier == 10

    def test_claude_haiku_4_5(self):
        assert CLAUDE_HAIKU_4_5.provider == Provider.ANTHROPIC
        assert CLAUDE_HAIKU_4_5.cost_per_input_token == 1.00
        assert CLAUDE_HAIKU_4_5.cost_per_output_token == 5.00
        assert CLAUDE_HAIKU_4_5.avg_latency_ms == 600
        assert CLAUDE_HAIKU_4_5.quality_tier == 6
        assert CLAUDE_HAIKU_4_5.max_complexity == 0.5

    def test_claude_opus_4_6(self):
        assert CLAUDE_OPUS_4_6.provider == Provider.ANTHROPIC
        assert CLAUDE_OPUS_4_6.cost_per_input_token == 5.00
        assert CLAUDE_OPUS_4_6.cost_per_output_token == 25.00
        assert CLAUDE_OPUS_4_6.avg_latency_ms == 2200
        assert CLAUDE_OPUS_4_6.context_window == 410_000
        assert CLAUDE_OPUS_4_6.quality_tier == 10

    def test_llama_3_3_70b(self):
        assert LLAMA_3_3_70B.provider == Provider.OLLAMA
        assert LLAMA_3_3_70B.cost_per_input_token == 0.0
        assert LLAMA_3_3_70B.cost_per_output_token == 0.0
        assert LLAMA_3_3_70B.avg_latency_ms == 1200
        assert LLAMA_3_3_70B.quality_tier == 8
        assert LLAMA_3_3_70B.max_complexity == 0.8

    def test_llama_3_1_8b(self):
        assert LLAMA_3_1_8B.provider == Provider.OLLAMA
        assert LLAMA_3_1_8B.cost_per_input_token == 0.0
        assert LLAMA_3_1_8B.cost_per_output_token == 0.0
        assert LLAMA_3_1_8B.avg_latency_ms == 500
        assert LLAMA_3_1_8B.quality_tier == 5
        assert LLAMA_3_1_8B.max_complexity == 0.4

    def test_context_windows(self):
        for m in ALL_MODELS:
            if m.provider == Provider.ANTHROPIC:
                if m.model_id == "claude-opus-4.6":
                    assert m.context_window == 410_000
                else:
                    assert m.context_window == 200_000
            elif m.provider == Provider.OPENAI:
                assert m.context_window == 128_000
            elif m.provider == Provider.OLLAMA:
                assert m.context_window == 128_000

    def test_quality_tiers(self):
        tiers = {m.model_id: m.quality_tier for m in ALL_MODELS}
        assert tiers["gpt-4o"] == 9
        assert tiers["gpt-4o-mini"] == 7
        assert tiers["o1-mini"] == 9
        assert tiers["claude-3.5-sonnet"] == 9
        assert tiers["claude-sonnet-4.6"] == 10
        assert tiers["claude-haiku-4.5"] == 6
        assert tiers["claude-opus-4.6"] == 10
        assert tiers["llama3.3-70b"] == 8
        assert tiers["llama3.1-8b"] == 5

    def test_latency_values(self):
        latencies = {m.model_id: m.avg_latency_ms for m in ALL_MODELS}
        assert latencies["gpt-4o"] == 1500
        assert latencies["gpt-4o-mini"] == 800
        assert latencies["o1-mini"] == 3000
        assert latencies["claude-3.5-sonnet"] == 1800
        assert latencies["claude-sonnet-4.6"] == 1700
        assert latencies["claude-haiku-4.5"] == 600
        assert latencies["claude-opus-4.6"] == 2200
        assert latencies["llama3.3-70b"] == 1200
        assert latencies["llama3.1-8b"] == 500

    def test_zero_cost_ollama(self):
        assert LLAMA_3_3_70B.estimate_cost(1000, 500) == 0.0
        assert LLAMA_3_1_8B.estimate_cost(1_000_000, 1_000_000) == 0.0

    def test_multimodal_support(self):
        assert GPT4O.supports_multimodal is True
        assert GPT4O_MINI.supports_multimodal is True
        assert O1_MINI.supports_multimodal is False
        assert CLAUDE_HAIKU_4_5.supports_multimodal is True
        assert LLAMA_3_1_8B.supports_multimodal is False


class TestRegistry:
    def test_registry_size(self):
        assert len(MODEL_REGISTRY) == 9

    def test_registry_keys(self):
        expected_keys = {
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "openai/o1-mini",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-sonnet-4.6",
            "anthropic/claude-haiku-4.5",
            "anthropic/claude-opus-4.6",
            "ollama/llama3.3-70b",
            "ollama/llama3.1-8b",
        }
        assert set(MODEL_REGISTRY.keys()) == expected_keys

    def test_get_model_found(self):
        m = get_model("openai/gpt-4o")
        assert m is GPT4O

    def test_get_model_not_found(self):
        with pytest.raises(ValueError, match="Model 'foo/bar' not found"):
            get_model("foo/bar")

    def test_get_model_error_contains_available(self):
        with pytest.raises(ValueError) as exc:
            get_model("nope/x")
        msg = str(exc.value)
        assert "openai/gpt-4o" in msg
        assert "ollama/llama3.1-8b" in msg

    def test_get_models_by_provider_openai(self):
        models = get_models_by_provider(Provider.OPENAI)
        assert len(models) == 3
        assert all(m.provider == Provider.OPENAI for m in models)

    def test_get_models_by_provider_anthropic(self):
        models = get_models_by_provider(Provider.ANTHROPIC)
        assert len(models) == 4
        assert all(m.provider == Provider.ANTHROPIC for m in models)

    def test_get_models_by_provider_ollama(self):
        models = get_models_by_provider(Provider.OLLAMA)
        assert len(models) == 2
        assert all(m.provider == Provider.OLLAMA for m in models)


class TestCheapestModel:
    def test_simple_complexity_returns_cheapest(self):
        m = get_cheapest_model_for_complexity(0.1)
        assert m.cost_per_input_token == 0.0
        assert m in (LLAMA_3_1_8B, LLAMA_3_3_70B)

    def test_medium_complexity(self):
        m = get_cheapest_model_for_complexity(0.5)
        assert m is LLAMA_3_3_70B

    def test_high_complexity(self):
        m = get_cheapest_model_for_complexity(0.9)
        capable_models = [m for m in ALL_MODELS if m.max_complexity >= 0.9]
        assert m in capable_models

    def test_fallback_to_gpt4o(self):
        m = get_cheapest_model_for_complexity(1.5)
        assert m is GPT4O

    def test_edge_complexity(self):
        m = get_cheapest_model_for_complexity(0.0)
        assert m is not None
        assert m.min_complexity <= 0.0 <= m.max_complexity

    def test_negative_complexity(self):
        m = get_cheapest_model_for_complexity(-0.1)
        assert m is GPT4O


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
