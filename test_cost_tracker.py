from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from unittest.mock import AsyncMock
import pytest

from storage.duckdb_logger import (
    BASELINE_OUTPUT_PER_MTOK,
    BASELINE_INPUT_PER_MTOK,
    DuckDBLogger,
    hash_prompt,
)


@pytest.fixture
def logger():
    return DuckDBLogger(":memory:")


class TestHash:
    def test_hash_is_sha256(self):
        h = hash_prompt("hello world")
        assert h == hashlib.sha256(b"hello world").hexdigest()
        assert len(h) == 64

    def test_hash_deterministic(self):
        assert hash_prompt("test") == hash_prompt("test")

    def test_hash_differs_for_different_inputs(self):
        assert hash_prompt("a") != hash_prompt("b")


class TestSchema:
    def test_table_created_on_init(self):
        logger = DuckDBLogger(":memory:")
        tables = logger.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert ("llm_requests",) in tables

    def test_columns_match_spec(self, logger):
        cols = [r[0] for r in logger.conn.execute("DESCRIBE llm_requests").fetchall()]
        expected = [
            "request_id", "timestamp", "prompt_hash", "prompt_preview",
            "complexity_tier", "routed_model", "baseline_model",
            "input_tokens", "output_tokens", "cost_usd", "baseline_cost_usd",
            "latency_ms", "quality_score", "escalation_flag", "success",
        ]
        assert cols == expected


class TestLogAndQuery:
    def test_log_one_request(self, logger):
        logger.log_request(
            request_id="req-001",
            prompt="What is 2+2?",
            complexity_tier="1",
            routed_model="gpt-4o-mini",
            baseline_model="gpt-4o",
            input_tokens=10,
            output_tokens=5,
            cost_usd=0.0000045,
            latency_ms=150,
            quality_score=1.0,
            escalation_flag=False,
            success=True,
        )
        summary = logger.get_summary()
        assert summary["total_requests"] == 1
        assert summary["routed_cost"] == 0.0000045

    def test_baseline_cost_correct(self, logger):
        logger.log_request(
            request_id="req-001", prompt="test",
            complexity_tier="1", routed_model="a", baseline_model="gpt-4o",
            input_tokens=1_000_000, output_tokens=1_000_000,
            cost_usd=10.0, latency_ms=100, quality_score=1.0,
            escalation_flag=False, success=True,
        )
        summary = logger.get_summary()
        # baseline = 1M * ($2.50/M) + 1M * ($10.00/M) = $12.50
        assert summary["baseline_cost"] == pytest.approx(12.50)
        # reduction = (12.50 - 10.0) / 12.50 * 100 = 20%
        assert summary["cost_reduction_pct"] == pytest.approx(20.0)

    def test_multiple_rows_aggregate(self, logger):
        for i in range(5):
            logger.log_request(
                request_id=f"req-{i:03d}", prompt=f"prompt {i}",
                complexity_tier=str(i % 3 + 1), routed_model="m",
                baseline_model="gpt-4o",
                input_tokens=100, output_tokens=50,
                cost_usd=0.001, latency_ms=100.0 + i * 10,
                quality_score=0.9 + i * 0.02, escalation_flag=i % 2 == 0,
                success=True,
            )
        summary = logger.get_summary()
        assert summary["total_requests"] == 5
        assert summary["routed_cost"] == 0.005
        assert summary["escalations"] == 3  # i=0,2,4 are even

    def test_empty_db_summary(self, logger):
        summary = logger.get_summary()
        assert summary["total_requests"] == 0
        assert summary["cost_reduction_pct"] == 0.0


class TestGrafanaQueries:
    @pytest.fixture(autouse=True)
    def seed_data(self, logger):
        for i in range(30):
            tier = str((i % 3) + 1)
            escalated = i % 5 == 0
            # Baseline = GPT-4o at 2.50/M in + 10.00/M out
            # Tier 1: 100 tok in, 20 tok out — baseline $0.00045, routed 70% cheaper
            # Tier 2: 500 tok in, 150 tok out — baseline $0.00275, routed 40% cheaper
            # Tier 3: 2000 tok in, 800 tok out — baseline $0.013, routed 10% cheaper
            tok_map = {"1": (100, 20, 0.7), "2": (500, 150, 0.6), "3": (2000, 800, 0.9)}
            in_tok, out_tok, cost_factor = tok_map[tier]
            baseline = (in_tok / 1e6) * 2.50 + (out_tok / 1e6) * 10.00
            cost_usd = round(baseline * cost_factor, 6)
            logger.log_request(
                request_id=f"r{i:03d}", prompt=f"p{i}",
                complexity_tier=tier, routed_model=f"model-{tier}",
                baseline_model="gpt-4o", input_tokens=in_tok, output_tokens=out_tok,
                cost_usd=cost_usd,
                latency_ms=100.0, quality_score=1.0 - 0.1 * escalated,
                escalation_flag=escalated, success=True,
            )
        return logger

    def test_cost_reduction_headline(self, seed_data):
        conn = seed_data.conn
        row = conn.execute("""
        SELECT 100.0 * (SUM(baseline_cost_usd) - SUM(cost_usd)) / NULLIF(SUM(baseline_cost_usd), 0)
        FROM llm_requests
        """).fetchone()
        assert row[0] > 0  # positive savings

    def test_cost_by_tier(self, seed_data):
        conn = seed_data.conn
        rows = conn.execute("""
        SELECT complexity_tier, COUNT(*), SUM(cost_usd)
        FROM llm_requests GROUP BY 1 ORDER BY 1
        """).fetchall()
        assert len(rows) == 3
        # Tier 3 costs more per call, but fewer calls
        tier3_cost = [r for r in rows if r[0] == "3"][0][2]
        tier1_cost = [r for r in rows if r[0] == "1"][0][2]
        assert tier3_cost > tier1_cost

    def test_escalation_rate(self, seed_data):
        conn = seed_data.conn
        row = conn.execute("""
        SELECT COUNT(*), SUM(CASE WHEN escalation_flag THEN 1 ELSE 0 END)
        FROM llm_requests
        """).fetchone()
        assert row[0] == 30
        assert row[1] == 6  # i%5==0 for 0..29

    def test_model_quality_scatter(self, seed_data):
        conn = seed_data.conn
        rows = conn.execute("""
        SELECT routed_model, AVG(quality_score), COUNT(*)
        FROM llm_requests GROUP BY 1 ORDER BY 1
        """).fetchall()
        assert len(rows) == 3  # model-1, model-2, model-3
        # model with escalations has lower avg quality
        for model, avg_q, count in rows:
            assert avg_q > 0.0 and avg_q <= 1.0

    def test_daily_trend(self, seed_data):
        conn = seed_data.conn
        rows = conn.execute("""
        SELECT DATE_TRUNC('day', timestamp) AS day,
               SUM(cost_usd) AS routed_cost,
               SUM(baseline_cost_usd) AS baseline_cost
        FROM llm_requests GROUP BY 1 ORDER BY 1
        """).fetchall()
        assert len(rows) >= 1
        assert rows[0][1] > 0  # routed cost > 0


class TestVerifierIntegration:
    def test_verifier_has_logger(self):
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()
        assert hasattr(pipeline, "_db_logger")
        assert pipeline._db_logger is not None

    @pytest.mark.asyncio
    async def test_process_calls_log_request(self):
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()
        pipeline._db_logger = DuckDBLogger(":memory:")

        pipeline._run_oracle = AsyncMock(return_value=("oracle", "claude-opus-4.6"))
        pipeline._run_judge = AsyncMock(return_value=(1.0, "perfect"))
        pipeline._record_failure = AsyncMock()

        await pipeline.enqueue("test prompt", "response", {
            "model": "gpt-4o-mini", "tier": 1, "input_tokens": 10, "output_tokens": 5
        })
        await pipeline.process_next()

        summary = pipeline._db_logger.get_summary()
        assert summary["total_requests"] == 1
