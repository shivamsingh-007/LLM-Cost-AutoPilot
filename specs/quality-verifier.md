# Spec: Quality Verification Loop

## Objective
Add an async quality-verification loop that catches routing failures. After each LLM response is served, a background job re-runs the prompt on the highest-quality model, scores agreement via LLM-as-judge, auto-escalates failures to a better model, logs traces to Langfuse (optional), and feeds failures back into the classifier dataset (flywheel).

Success: routing failures are detected, logged, and fed back for retraining — no user-facing quality regression goes unnoticed.

## Tech Stack
- Python 3.10+, same venv
- `langfuse` Python SDK (optional, guarded by try/except)
- All LLM calls via `UnifiedLLMInterface.send_request` (provider-agnostic)
- asyncio for background queue (no Celery/Redis for POC)

## Commands
```
Test:   python -m pytest test_verifier.py -v
Run worker: python -c "import asyncio; from verifier.async_verifier import verifier_worker; asyncio.run(verifier_worker())"
All tests: python -m pytest test_verifier.py test_models_config.py test_unified_interface.py test_classifier.py test_benchmark.py -v
```

## Project Structure
```
verifier/
  __init__.py
  async_verifier.py      → Queue, worker, process_job (verifier loop core)
  judge_prompts.py       → Deterministic judge prompt templates
  reroute_handler.py     → Auto-escalation: re-run on highest-tier model
  langfuse_logger.py     → Langfuse trace wrapper (no-op fallback)
  classifier_feedback.py → Append failures to complexity_labels.csv (flywheel)
config/
  __init__.py
  routing_map.yaml       → (existing) Tier→model mappings
  settings.py            → NEW: Settings from env (Langfuse keys, toggle)
test_verifier.py          → NEW: Tests for verifier pipeline
requirements.txt          → +langfuse
```

## Code Style

```python
class VerifierJob:
    """A single verification unit: prompt + response + metadata."""

    AGREEMENT_THRESHOLD = 0.8

    def __init__(self, prompt: str, response_text: str, metadata: dict):
        self.prompt = prompt
        self.response_text = response_text
        self.metadata = metadata
```

- Same conventions as Day 1/2: PascalCase classes, snake_case methods/functions
- Public methods documented; internals prefixed `_`
- Imports: stdlib → third-party → local

## Testing Strategy

| Level | File | What |
|-------|------|------|
| Unit | `test_verifier.py` | Verify judge prompt formatting, failure CSV append, Langfuse no-op behavior, settings parse |
| Integration | `test_verifier.py` | Full pipeline: enqueue → judge parse → feedback append (mocked LLM calls) |

No live API calls in tests. All LLM responses are mocked.

## Boundaries

- **Always:** Guard Langfuse imports with try/except. Write routing_failures.csv with matching schema. Run tests before committing.
- **Ask first:** Adding non-Python dependencies (Redis, Celery). Changing AGREEMENT_THRESHOLD. Making Langfuse required.
- **Never:** Block user response on verifier. Hardcode API keys. Remove no-op fallback for Langfuse.

## Success Criteria

1. `verifier/async_verifier.py` has an asyncio-based queue + worker + process_job
2. `verifier/judge_prompts.py` returns a deterministic prompt string with scoring rubric
3. `verifier/reroute_handler.py` calls `send_request` on highest `quality_tier` model
4. `verifier/langfuse_logger.py` works with and without Langfuse SDK installed
5. `verifier/classifier_feedback.py` appends failures to `data/complexity_labels.csv` using existing `prompt,task_type,complexity_score,complexity_tier` schema
6. `config/settings.py` reads `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `ENABLE_LANGFUSE` from env
7. `test_verifier.py` passes all tests with mocked LLM calls
8. No regression on existing 70 tests

## Open Questions

None — spec covers verifier pipeline as discussed.
