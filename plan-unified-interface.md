# Implementation Plan: Unified Model Interface

## Global Constraints
- Python 3.10+ target
- Provider SDKs are optional — graceful degradation if missing
- True async: use `AsyncOpenAI`, `AsyncAnthropic`, `ollama.AsyncClient` — never sync SDK in async wrapper
- API keys from env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- Ollama host from `OLLAMA_HOST` env var (default `http://localhost:11434`)
- On any exception: return `Response(success=False, error_message=str(e))` — never raise
- Ollama token estimation: `len(prompt.split()) * 1.3` for input, same for output
- Dependencies: `openai>=1.60.0`, `anthropic>=0.45.0`, `ollama>=0.4.0`, `python-dotenv>=1.0.0`
- No streaming support in this phase (nice-to-have, deferred)
- Work directory: `C:\Users\shiva\OneDrive\Documents\15 AI projects\LLM Cost Autopilot`

## Task 1: models_config.py

**File:** `models_config.py`

**Requirements:**
1. `Provider` enum with `OPENAI`, `ANTHROPIC`, `OLLAMA`
2. `ModelConfig` dataclass with all fields from spec:
   - `provider: Provider`
   - `model_id: str`, `display_name: str`
   - `cost_per_input_token: float`, `cost_per_output_token: float` (per 1M tokens)
   - `avg_latency_ms: float`, `context_window: int`, `max_output_tokens: int`
   - `quality_tier: int`
   - `supports_coding: bool = True`, `supports_reasoning: bool = True`, `supports_multimodal: bool = False`
   - `min_complexity: float = 0.0`, `max_complexity: float = 1.0`
3. Methods on ModelConfig: `cost_per_token(is_output)`, `estimate_cost(input_tokens, output_tokens)`, `to_dict()`
4. 8 model instances with real 2026 pricing:
   - **OpenAI:** GPT-4o ($2.50/$10.00), GPT-4o Mini ($0.15/$0.60), o1-mini ($3.00/$12.00)
   - **Anthropic:** Claude 3.5 Sonnet ($3.00/$15.00), Claude Sonnet 4.6 ($3.00/$15.00), Claude Haiku 4.5 ($1.00/$5.00), Claude Opus 4.6 ($5.00/$25.00)
   - **Ollama:** Llama 3.3 70B ($0/$0), Llama 3.1 8B ($0/$0)
5. `MODEL_REGISTRY` dict keyed by `"provider/model-id"`
6. `get_model(model_id)` — raises ValueError with available list if not found
7. `get_models_by_provider(provider)` — returns list
8. `get_cheapest_model_for_complexity(complexity)` — cheapest capable model, fallback to GPT-4o
9. Latency values: GPT-4o (1500ms), GPT-4o Mini (800ms), o1-mini (3000ms), Claude 3.5 Sonnet (1800ms), Claude 4 Sonnet (1700ms), Haiku (600ms), Opus (2200ms), Llama 3.3 70B (1200ms), Llama 3.1 8B (500ms)
10. Context windows: OpenAI (128k), Anthropic (200k except Opus 410k), Ollama (128k)
11. Quality tiers: GPT-4o (9), Mini (7), o1-mini (9), Sonnet 3.5 (9), Sonnet 4.6 (10), Haiku (6), Opus (10), Llama 3.3 (8), Llama 3.1 (5)
12. Complexity ranges for each model from the spec

## Task 2: unified_interface.py

**File:** `unified_interface.py`

**Requirements:**
1. `Response` dataclass with `output`, `tokens` dict, `latency_ms`, `cost_usd`, `model_id`, `provider`, `success`, `error_message`, `to_dict()`
2. `UnifiedLLMInterface` class:
   - `__init__()` initializes `AsyncOpenAI`, `AsyncAnthropic`, `ollama.AsyncClient` — try/except for ImportError, client = None on failure
   - `async send_request(prompt, model_config, system_prompt="", temperature=0.7, max_tokens=1000)` returning `Response`
   - Routes to `_call_openai`, `_call_anthropic`, `_call_ollama` based on provider
   - `_call_openai`: uses `await self.openai_client.chat.completions.create(...)`, returns content + token counts
   - `_call_anthropic`: uses `await self.anthropic_client.messages.create(...)`, returns content + token counts
   - `_call_ollama`: uses `await self.ollama_client.chat(...)`, estimates tokens via word count * 1.3
   - On any exception: return `Response(success=False, error_message=str(e))`
   - Calculate latency from `time.time()` delta
   - Calculate cost via `model_config.estimate_cost(input_tokens, output_tokens)`

## Task 3: test_unified_interface.py

**File:** `test_unified_interface.py`

**Requirements:**
1. 10 test prompts with varying complexity (0.2 to 0.9):
   - Simple Query, Coding Task, Math Problem, Creative Writing, Analysis, Complex Reasoning, Long Context, JSON Generation, Debugging, Multi-step Task
2. Test all 8 models: GPT-4o, GPT-4o Mini, Claude 3.5 Sonnet, Claude Haiku, Llama 3.3 70B, Llama 3.1 8B, o1-mini, Claude Opus 4.6, Claude Sonnet 4.6
3. Run with `asyncio.run()`
4. Print detailed results per model+prompt
5. Print summary table: Model | Success | Avg Latency | Avg Cost | Avg Tokens
6. Print cost comparison vs GPT-4o baseline
7. Save results to `test_results.csv`
8. Graceful handling of missing API keys (caught by `success=False`)

## Task 4: requirements.txt and .env.example

**Files:** `requirements.txt`, `.env.example`

**Requirements:**
1. `requirements.txt` with: `openai>=1.60.0`, `anthropic>=0.45.0`, `ollama>=0.4.0`, `python-dotenv>=1.0.0`
2. `.env.example` with: `OPENAI_API_KEY=your_openai_key_here`, `ANTHROPIC_API_KEY=your_anthropic_key_here`, `OLLAMA_HOST=http://localhost:11434`
