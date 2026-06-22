# Task 3: Benchmark Runner — Report

## Files Created

| File | Purpose |
|------|---------|
| `run_benchmark.py` | Main async benchmark script — 10 prompts × 9 models, concurrent per model, results to CSV |
| `test_benchmark.py` | Unit tests for prompt data structure and CSV writing (no live API calls) |

## Design Decisions

### Prompt Structure
- 10 prompts defined as `BenchmarkPrompt` dataclass with `prompt_id`, `prompt_name`, `prompt_text`, `system_prompt`, `complexity`
- IDs P01–P10, all unique
- Complexity spread across 0.2–0.9 covering 7 distinct values
- 5 prompts use system prompts, 5 don't — exercises both code paths

### Concurrency
- `asyncio.gather` runs all 10 prompts concurrently per model
- No `return_exceptions=True` — `send_request` already catches all exceptions and returns `success=False`

### Error Handling
- Missing API keys → SDK init fails → `send_request` catches → `success=False` with error message
- No special-casing: errors flow through the existing `Response` error path

### CSV Output
- `test_results.csv` has exactly these columns: `model, prompt_id, prompt_name, complexity, success, latency_ms, cost_usd, tokens_total, output_length, error`
- No `output` column (kept only for potential console display)

### Summary
- Per-model summary table: Model | Success | Avg Latency | Avg Cost | Avg Tokens
- Cost comparison vs GPT-4o baseline with % savings

## Test Coverage

`test_benchmark.py` covers:
- Prompt list has exactly 10 entries
- All required fields present on each prompt
- All prompt IDs are unique
- Complexity values cover expected set {0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
- Mix of system prompts present/absent
- CSV writing produces correct columns
- Output column excluded from CSV
- Correct number of CSV rows for multi-row data

## Verification

```
pytest test_benchmark.py -v
```
