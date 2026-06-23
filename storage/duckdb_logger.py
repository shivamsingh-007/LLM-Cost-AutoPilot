from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import duckdb


BASELINE_INPUT_PER_MTOK = 2.50
BASELINE_OUTPUT_PER_MTOK = 10.00


def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


@dataclass
class RequestLog:
    request_id: str
    timestamp: datetime
    prompt_hash: str
    prompt_preview: str
    complexity_tier: str
    routed_model: str
    baseline_model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    baseline_cost_usd: float
    latency_ms: float
    quality_score: float
    escalation_flag: bool
    success: bool


class DuckDBLogger:
    def __init__(self, db_path: str = "data/llm_autopilot.duckdb"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_requests (
          request_id VARCHAR PRIMARY KEY,
          timestamp TIMESTAMP,
          prompt_hash VARCHAR,
          prompt_preview VARCHAR,
          complexity_tier VARCHAR,
          routed_model VARCHAR,
          baseline_model VARCHAR,
          input_tokens INTEGER,
          output_tokens INTEGER,
          cost_usd DOUBLE,
          baseline_cost_usd DOUBLE,
          latency_ms DOUBLE,
          quality_score DOUBLE,
          escalation_flag BOOLEAN,
          success BOOLEAN
        );
        """)

    @staticmethod
    def estimate_baseline_cost(input_tokens: int, output_tokens: int) -> float:
        return (
            (input_tokens / 1_000_000) * BASELINE_INPUT_PER_MTOK
            + (output_tokens / 1_000_000) * BASELINE_OUTPUT_PER_MTOK
        )

    def log_request(
        self,
        request_id: str,
        prompt: str,
        complexity_tier: str,
        routed_model: str,
        baseline_model: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        latency_ms: float,
        quality_score: float,
        escalation_flag: bool,
        success: bool,
        ts: Optional[datetime] = None,
    ):
        ts = ts or datetime.now(timezone.utc)
        baseline_cost_usd = self.estimate_baseline_cost(input_tokens, output_tokens)

        self.conn.execute("""
        INSERT OR REPLACE INTO llm_requests VALUES (
          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, [
            request_id,
            ts.isoformat(),
            hash_prompt(prompt),
            prompt[:160],
            complexity_tier,
            routed_model,
            baseline_model,
            input_tokens,
            output_tokens,
            cost_usd,
            baseline_cost_usd,
            latency_ms,
            quality_score,
            escalation_flag,
            success,
        ])

    def get_summary(self):
        q = self.conn.execute("""
        SELECT
          COUNT(*) AS total_requests,
          COALESCE(SUM(cost_usd), 0) AS routed_cost,
          COALESCE(SUM(baseline_cost_usd), 0) AS baseline_cost,
          CASE
            WHEN COALESCE(SUM(baseline_cost_usd), 0) = 0 THEN 0
            ELSE 100.0 * (SUM(baseline_cost_usd) - SUM(cost_usd)) / SUM(baseline_cost_usd)
          END AS cost_reduction_pct,
          COALESCE(AVG(latency_ms), 0) AS avg_latency_ms,
          COALESCE(AVG(quality_score), 0) AS avg_quality_score,
          COALESCE(SUM(CASE WHEN escalation_flag THEN 1 ELSE 0 END), 0) AS escalations
        FROM llm_requests
        """).fetchone()

        return {
            "total_requests": int(q[0]),
            "routed_cost": float(q[1]),
            "baseline_cost": float(q[2]),
            "cost_reduction_pct": float(q[3]),
            "avg_latency_ms": float(q[4]),
            "avg_quality_score": float(q[5]),
            "escalations": int(q[6]),
        }
