# Spec: DuckDB Cost Tracker

## Objective
Add a DuckDB-backed event store that logs every routed LLM request. Compute the headline "cost reduction vs GPT-4o baseline" metric. Expose Grafana-friendly SQL queries for dashboard panels. Wire logging into the VerifierPipeline so every verified request is automatically recorded.

## Tech Stack
- Python 3.10+, same venv
- DuckDB >= 1.0 (embedded SQL, no server)
- `duckdb` package added to requirements.txt

## Commands
```
Test: python -m pytest test_cost_tracker.py -v
Query: python -c "from storage.duckdb_logger import DuckDBLogger; l=DuckDBLogger(':memory:'); print(l.get_summary())"
```

## Project Structure
```
storage/
  __init__.py
  duckdb_logger.py          → DuckDBLogger class (schema, log, summary, queries)
test_cost_tracker.py         → Tests for log, summary, queries, integration with verifier
data/
  llm_autopilot.duckdb       → DuckDB database file (gitignored)
.gitignore                   → +data/*.duckdb
requirements.txt             → +duckdb
```

## Code Style

```python
class DuckDBLogger:
    """Logs LLM request metrics to DuckDB."""

    BASELINE_INPUT_PER_MTOK = 2.50
    BASELINE_OUTPUT_PER_MTOK = 10.00

    def __init__(self, db_path: str = "data/llm_autopilot.duckdb"):
        ...
```

Same conventions as existing code. Public methods: `log_request()`, `get_summary()`.

## Testing Strategy

| Level | File | What |
|-------|------|------|
| Unit | `test_cost_tracker.py` | Schema creation, log a row, get_summary, hash function, baseline cost calc, Grafana queries |
| Integration | `test_cost_tracker.py` | Logger with `:memory:` DuckDB, multi-row aggregation, tier breakdown |
| Verifier integration | `test_verifier.py` | VerifierPipeline calls logger after processing (existing test updated) |

## Boundaries

- **Always:** Use `:memory:` DuckDB in tests. Gitignore `*.duckdb` files. Log after response, never before.
- **Ask first:** Changing baseline pricing strategy. Adding new columns to schema. Removing old data.
- **Never:** Store full prompt text beyond 160-char preview. Block the response on DB write. Hardcode DB path.

## Success Criteria

1. `DuckDBLogger` creates the `llm_requests` table on init
2. `log_request()` inserts a row with all 15 columns
3. `get_summary()` returns total_requests, routed_cost, baseline_cost, cost_reduction_pct, avg_latency_ms, avg_quality_score, escalations
4. Cost reduction % computed correctly: `100 * (baseline - routed) / baseline`
5. Grafana queries (daily trend, tier breakdown, escalation rate, model quality scatter) produce correct results
6. VerifierPipeline calls `log_request()` after `_process()` completes
7. All existing tests still pass

## Open Questions

None — spec covers DuckDB schema, logger, queries, and verifier integration as discussed.
