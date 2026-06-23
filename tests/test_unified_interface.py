from __future__ import annotations

from unittest.mock import AsyncMock, patch, MagicMock, ANY
import pytest

from core.models_config import ModelConfig, Provider, GPT4O, GPT4O_MINI, CLAUDE_HAIKU_4_5
from core.unified_interface import Response, UnifiedLLMInterface


class TestResponseDataclass:
    def test_default_success(self):
        r = Response(output="hello")
        assert r.success is True
        assert r.error_message == ""
        assert r.tokens == {"input": 0, "output": 0}

    def test_to_dict(self):
        r = Response(
            output="test",
            tokens={"input": 10, "output": 20},
            latency_ms=100.0,
            cost_usd=0.005,
            model_id="gpt-4o",
            provider="openai",
            success=True,
        )
        d = r.to_dict()
        assert d["output"] == "test"
        assert d["tokens"] == {"input": 10, "output": 20}
        assert d["latency_ms"] == 100.0
        assert d["cost_usd"] == 0.005
        assert d["model_id"] == "gpt-4o"
        assert d["provider"] == "openai"
        assert d["success"] is True
        assert d["error_message"] == ""

    def test_to_dict_error(self):
        r = Response(output="", success=False, error_message="something broke")
        d = r.to_dict()
        assert d["success"] is False
        assert d["error_message"] == "something broke"


class TestUnifiedLLMInterfaceInit:
    def test_init_does_not_import_sdks(self):
        llm = UnifiedLLMInterface()
        assert llm._openai_client is None
        assert llm._anthropic_client is None
        assert llm._ollama_client is None

    @patch("builtins.__import__", side_effect=ImportError("no openai"))
    def test_get_openai_returns_none_on_import_error(self, mock_import):
        llm = UnifiedLLMInterface()
        assert llm._get_openai() is None

    @patch("builtins.__import__", side_effect=ImportError("no anthropic"))
    def test_get_anthropic_returns_none_on_import_error(self, mock_import):
        llm = UnifiedLLMInterface()
        assert llm._get_anthropic() is None

    @patch("builtins.__import__", side_effect=ImportError("no ollama"))
    def test_get_ollama_returns_none_on_import_error(self, mock_import):
        llm = UnifiedLLMInterface()
        assert llm._get_ollama() is None

    @patch("builtins.__import__")
    def test_get_openai_creates_client(self, mock_import):
        mock_mod = MagicMock()
        mock_mod.AsyncOpenAI = MagicMock(return_value="openai_client")
        mock_import.return_value = mock_mod
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
            llm = UnifiedLLMInterface()
            assert llm._get_openai() == "openai_client"
            mock_mod.AsyncOpenAI.assert_called_once_with(api_key="sk-test")


@pytest.mark.asyncio
class TestRouting:
    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_routes_to_openai(self, mock_call_openai):
        mock_call_openai.return_value = ("openai output", {"input": 10, "output": 20})
        llm = UnifiedLLMInterface()
        r = await llm.send_request("hello", GPT4O)
        mock_call_openai.assert_awaited_once()
        assert r.success is True
        assert r.output == "openai output"
        assert r.provider == "openai"

    @patch.object(UnifiedLLMInterface, "_call_anthropic", new_callable=AsyncMock)
    async def test_routes_to_anthropic(self, mock_call_anthropic):
        mock_call_anthropic.return_value = ("anthropic output", {"input": 15, "output": 25})
        llm = UnifiedLLMInterface()
        r = await llm.send_request("hello", CLAUDE_HAIKU_4_5)
        mock_call_anthropic.assert_awaited_once()
        assert r.success is True
        assert r.output == "anthropic output"
        assert r.provider == "anthropic"

    @patch.object(UnifiedLLMInterface, "_call_ollama", new_callable=AsyncMock)
    async def test_routes_to_ollama(self, mock_call_ollama):
        mock_call_ollama.return_value = ("ollama output", {"input": 5, "output": 10})
        llm = UnifiedLLMInterface()
        model = ModelConfig(
            provider=Provider.OLLAMA,
            model_id="llama3.1-8b",
            display_name="Test",
            cost_per_input_token=0.0,
            cost_per_output_token=0.0,
            avg_latency_ms=500,
            context_window=128_000,
            max_output_tokens=8_192,
            quality_tier=5,
        )
        r = await llm.send_request("hello", model)
        mock_call_ollama.assert_awaited_once()
        assert r.success is True
        assert r.output == "ollama output"
        assert r.provider == "ollama"


@pytest.mark.asyncio
class TestErrorHandling:
    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_error_returns_success_false(self, mock_call_openai):
        mock_call_openai.side_effect = RuntimeError("API failure")
        llm = UnifiedLLMInterface()
        r = await llm.send_request("hello", GPT4O)
        assert r.success is False
        assert "API failure" in r.error_message
        assert r.output == ""

    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_error_still_provides_model_info(self, mock_call_openai):
        mock_call_openai.side_effect = RuntimeError("fail")
        llm = UnifiedLLMInterface()
        r = await llm.send_request("hello", GPT4O)
        assert r.model_id == "gpt-4o"
        assert r.provider == "openai"

    async def test_unknown_provider(self):
        llm = UnifiedLLMInterface()
        from enum import Enum
        class FakeProvider(Enum):
            FAKE = "fake"
        fake_model = ModelConfig(
            provider=FakeProvider.FAKE,
            model_id="fake",
            display_name="Fake",
            cost_per_input_token=0,
            cost_per_output_token=0,
            avg_latency_ms=0,
            context_window=0,
            max_output_tokens=0,
            quality_tier=0,
        )
        r = await llm.send_request("hello", fake_model)
        assert r.success is False
        assert "Unknown provider" in r.error_message


@pytest.mark.asyncio
class TestCostCalculation:
    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_cost_matches_estimate_cost(self, mock_call_openai):
        mock_call_openai.return_value = ("content", {"input": 100, "output": 50})
        llm = UnifiedLLMInterface()
        r = await llm.send_request("hello", GPT4O_MINI)
        expected = GPT4O_MINI.estimate_cost(100, 50)
        assert r.cost_usd == pytest.approx(expected)

    @patch.object(UnifiedLLMInterface, "_call_ollama", new_callable=AsyncMock)
    async def test_zero_cost_for_ollama(self, mock_call_ollama):
        mock_call_ollama.return_value = ("content", {"input": 100, "output": 50})
        llm = UnifiedLLMInterface()
        model = ModelConfig(
            provider=Provider.OLLAMA,
            model_id="test",
            display_name="Test",
            cost_per_input_token=0.0,
            cost_per_output_token=0.0,
            avg_latency_ms=500,
            context_window=128_000,
            max_output_tokens=8_192,
            quality_tier=5,
        )
        r = await llm.send_request("hello", model)
        assert r.cost_usd == 0.0


@pytest.mark.asyncio
class TestSendRequestParameters:
    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_passes_system_prompt(self, mock_call_openai):
        mock_call_openai.return_value = ("content", {"input": 10, "output": 20})
        llm = UnifiedLLMInterface()
        await llm.send_request("hello", GPT4O, system_prompt="be helpful")
        mock_call_openai.assert_awaited_once()
        args, _ = mock_call_openai.call_args
        assert args[2] == "be helpful"

    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_passes_temperature_and_max_tokens(self, mock_call_openai):
        mock_call_openai.return_value = ("content", {"input": 10, "output": 20})
        llm = UnifiedLLMInterface()
        await llm.send_request("hello", GPT4O, temperature=0.3, max_tokens=500)
        mock_call_openai.assert_awaited_once_with("hello", GPT4O, "", 0.3, 500)

    @patch.object(UnifiedLLMInterface, "_call_openai", new_callable=AsyncMock)
    async def test_empty_prompt_returns_response(self, mock_call_openai):
        mock_call_openai.return_value = ("", {"input": 0, "output": 0})
        llm = UnifiedLLMInterface()
        r = await llm.send_request("", GPT4O)
        assert r.success is True
        assert r.output == ""
