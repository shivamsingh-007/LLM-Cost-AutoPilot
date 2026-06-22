# Unified Model Interface

## Objective
A single, async-native Python interface that abstracts away OpenAI, Anthropic, and Ollama provider SDKs behind one `send_request()` function. Returns a standardized `Response` dataclass with output, token usage, latency, and cost. Developers integrate once and route to any model without provider-specific code.

## Requirements

### Must Have
- `ModelConfig` dataclass with provider, model_id, pricing (per 1M tokens), latency, context window, quality tier, and complexity range
- Real 2026 pricing populated for 8 models: GPT-4o, GPT-4o Mini, o1-mini, Claude 3.5 Sonnet, Claude 4 Sonnet, Claude Haiku 4.5, Claude Opus 4.6, Llama 3.3 70B, Llama 3.1 8B
- `MODEL_REGISTRY` dict keyed by `"provider/model-id"` with `get_model()`, `get_models_by_provider()`, and `get_cheapest_model_for_complexity()` helpers
- `UnifiedLLMInterface` class with async `send_request(prompt, model_config, system_prompt, temperature, max_tokens)` returning a `Response` object
- True async implementation using `AsyncOpenAI`, `AsyncAnthropic`, and `ollama.AsyncClient` — no sync-with-async-wrapper anti-pattern
- `Response` dataclass with `output`, `tokens` dict, `latency_ms`, `cost_usd`, `model_id`, `provider`, `success`, `error_message`, and `to_dict()`
- `ModelConfig.estimate_cost(input_tokens, output_tokens)` returning total cost in USD
- Graceful failure: on any exception, return a `Response` with `success=False` and the error message, never raise
- 10 test prompts covering: simple query, coding, math, creative writing, analysis, complex reasoning, long context, JSON generation, debugging, multi-step task
- Test with all 8 models and output results table + CSV

### Nice to Have
- Streaming support in `send_request()` (future)
- Token counting via `tiktoken` for accurate input estimation (Ollama currently estimates via `len(prompt.split()) * 1.3`)

## Constraints
- Provider SDKs are optional — absence of a provider's SDK produces a clear warning, not a crash
- API keys read from environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Ollama host configurable via `OLLAMA_HOST` env var (default `http://localhost:11434`)
- Python 3.10+ target
- Dependencies: `openai>=1.60.0`, `anthropic>=0.45.0`, `ollama>=0.4.0`, `python-dotenv>=1.0.0`

## Edge Cases
- **Missing API key**: provider client fails to authenticate → `Response(success=False, error="401...")`
- **Unsupported model_id**: `get_model()` raises `ValueError` with list of available models
- **Provider SDK not installed**: client is `None`, request returns descriptive error (not `AttributeError`)
- **Network timeout**: exception caught, returned in `Response.error_message` with `success=False`
- **Ollama model not pulled locally**: Ollama returns 404/model-not-found → caught and returned as failed response
- **Zero-cost models (Ollama)**: `estimate_cost` correctly returns `$0.00`
- **Empty prompt**: each provider handles empty input messages — test behavior

## Definition of Done
- [ ] `models_config.py` with all 8 `ModelConfig` instances and registry functions
- [ ] `unified_interface.py` with `UnifiedLLMInterface` using `AsyncOpenAI`/`AsyncAnthropic`/`ollama.AsyncClient` and proper `await`
- [ ] `test_unified_interface.py` runs 10 prompts across all models
- [ ] Test suite runs without uncaught exceptions (failures are captured in `Response.success`)
- [ ] `test_results.csv` written after test run with per-request metrics
- [ ] Summary table printed showing success rate, avg latency, avg cost per model
- [ ] Cost comparison printed showing % savings vs GPT-4o
- [ ] `requirements.txt` and `.env.example` present

## Open Questions
- Should Ollama token estimation use `tiktoken` for accuracy, or is the word-count heuristic acceptable for Day 1?
