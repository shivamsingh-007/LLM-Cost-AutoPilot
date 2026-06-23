# Implementation Plan: Quality Verification Loop

## Overview
Add an async quality-verification pipeline: after each routed LLM response, a background job re-runs on the best model, scores agreement via LLM-as-judge, auto-escalates failures, logs to Langfuse (optional), and feeds failures back into the classifier dataset.

## Architecture Decisions
- **In-process asyncio.Queue** for POC (swap to Redis/Celery later)
- **Langfuse optional** — no-op fallback when SDK/env not configured
- **Failures append to existing CSV** — same `prompt,task_type,complexity_score,complexity_tier` schema
- **All verifier modules** under `verifier/` package for clean isolation

## Dependency Graph
```
config/settings.py
    │
    ├── verifier/judge_prompts.py          (zero deps)
    ├── verifier/langfuse_logger.py        (depends on settings)
    │
    ├── verifier/classifier_feedback.py    (depends on CSV path)
    │
    ├── verifier/reroute_handler.py        (depends on unified_interface, models_config, langfuse_logger)
    │
    ├── verifier/async_verifier.py         (depends on all above)
    │
    └── test_verifier.py                   (depends on async_verifier)
```

## Task List

### Phase 1: Foundation
- [ ] **Task 1:** `config/settings.py` + `requirements.txt` (+langfuse) + `verifier/` package init
- [ ] **Task 2:** `verifier/judge_prompts.py` — deterministic judge prompt templates
- [ ] **Task 3:** `verifier/langfuse_logger.py` — Langfuse trace wrapper with no-op fallback

### Checkpoint: Foundation
- [ ] All 3 modules import cleanly
- [ ] `config/settings` reads env vars, falls back to defaults
- [ ] `judge_prompts` returns valid judge prompt strings
- [ ] `langfuse_logger` handles both installed and missing SDK

### Phase 2: Core Verifier Components
- [ ] **Task 4:** `verifier/classifier_feedback.py` — append failures to `data/complexity_labels.csv`
- [ ] **Task 5:** `verifier/reroute_handler.py` — auto-escalate to highest-tier model
- [ ] **Task 6:** `verifier/async_verifier.py` — queue + worker + process_job (wires everything)

### Checkpoint: Core
- [ ] `classifier_feedback` appends rows to existing CSV without breaking schema
- [ ] `reroute_handler` calls `send_request` on the highest quality_tier model
- [ ] `async_verifier` enqueues, processes, and calls all subcomponents

### Phase 3: Tests
- [ ] **Task 7:** `test_verifier.py` — mocks all LLM calls, tests every verifier component
- [ ] Run full test suite: all 70+ existing tests + new verifier tests pass

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] No regression on existing 70 tests

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Langfuse SDK incompatible with existing deps | Med | Guard with try/except, tests run with no-op |
| CSV schema mismatch between failures and existing labels | Low | Already resolved: use existing `prompt,task_type,complexity_score,complexity_tier` |
| asyncio.Queue jobs lost on crash | Low | POC only. Document that production needs Redis/Celery |
