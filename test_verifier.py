from __future__ import annotations

import os
import tempfile
from unittest.mock import AsyncMock, patch

import pandas as pd
import pytest


class TestSettings:
    def test_defaults_when_env_missing(self):
        os.environ.pop("LANGFUSE_PUBLIC_KEY", None)
        os.environ.pop("LANGFUSE_SECRET_KEY", None)
        os.environ.pop("ENABLE_LANGFUSE", None)
        from config.settings import settings
        assert settings.ENABLE_LANGFUSE is False
        assert settings.LANGFUSE_PUBLIC_KEY == ""
        assert settings.LANGFUSE_SECRET_KEY == ""

    def test_reads_from_env(self):
        os.environ["ENABLE_LANGFUSE"] = "true"
        os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-test"
        os.environ["LANGFUSE_SECRET_KEY"] = "sk-test"
        # re-import to pick up new env
        import importlib
        import config.settings
        importlib.reload(config.settings)
        from config.settings import settings
        assert settings.ENABLE_LANGFUSE is True
        assert settings.LANGFUSE_PUBLIC_KEY == "pk-test"
        assert settings.LANGFUSE_SECRET_KEY == "sk-test"
        del os.environ["ENABLE_LANGFUSE"]
        del os.environ["LANGFUSE_PUBLIC_KEY"]
        del os.environ["LANGFUSE_SECRET_KEY"]
        importlib.reload(config.settings)


class TestJudgePrompts:
    def test_returns_string(self):
        from verifier.judge_prompts import agreement_judge_prompt
        prompt = agreement_judge_prompt("What is 2+2?", "4", "4")
        assert isinstance(prompt, str)
        assert len(prompt) > 50

    def test_contains_prompt_and_responses(self):
        from verifier.judge_prompts import agreement_judge_prompt
        prompt = agreement_judge_prompt("Hello?", "Candidate text", "Oracle text")
        assert "Hello?" in prompt
        assert "Candidate text" in prompt
        assert "Oracle text" in prompt

    def test_contains_scoring_rules(self):
        from verifier.judge_prompts import agreement_judge_prompt
        prompt = agreement_judge_prompt("x", "y", "z")
        assert "agreement" in prompt.lower()
        assert "0." in prompt  # float scores

    def test_requests_json_output(self):
        from verifier.judge_prompts import agreement_judge_prompt
        prompt = agreement_judge_prompt("x", "y", "z")
        assert "{" in prompt and "}" in prompt


class TestLangfuseLogger:
    def test_noop_when_disabled(self):
        from verifier.langfuse_logger import LangfuseLogger
        logger = LangfuseLogger()
        # Should not raise
        logger.log_verification(prompt="test", agreement=0.9)
        logger.log_rerun(original_model="a", escalated_model="b")
        logger.log_error("tag", {"key": "val"})

    def test_detects_missing_sdk(self):
        with patch.dict("sys.modules", {"langfuse": None}):
            import importlib
            import verifier.langfuse_logger
            importlib.reload(verifier.langfuse_logger)
            from verifier.langfuse_logger import LangfuseLogger
            logger = LangfuseLogger()
            # No-op mode when langfuse not importable
            logger.log_verification(prompt="test")
            importlib.reload(verifier.langfuse_logger)  # restore


class TestClassifierFeedback:
    def test_append_failure_to_csv(self):
        import tempfile, os
        from verifier.classifier_feedback import record_routing_failure
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "complexity_labels.csv")
            pd.DataFrame(columns=["prompt", "task_type", "complexity_score", "complexity_tier"]).to_csv(csv_path, index=False)
            record = {
                "prompt": "test prompt",
                "agreement": 0.3,
                "candidate_model": "gpt-4o-mini",
                "oracle_model": "claude-opus-4.6",
            }
            record_routing_failure(record, labels_csv=csv_path)
            df = pd.read_csv(csv_path)
            assert len(df) == 1  # one data row (header not counted)
            row = df.iloc[0]
            assert row["prompt"] == "test prompt"
            assert row["task_type"] == "verifier_failure"
            assert row["complexity_tier"] == 3

    def test_appends_multiple_failures(self):
        from verifier.classifier_feedback import record_routing_failure
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "complexity_labels.csv")
            pd.DataFrame(columns=["prompt", "task_type", "complexity_score", "complexity_tier"]).to_csv(csv_path, index=False)
            for i in range(3):
                record_routing_failure({"prompt": f"p{i}", "agreement": 0.2}, labels_csv=csv_path)
            df = pd.read_csv(csv_path)
            assert len(df) == 3  # 3 data rows

    def test_creates_csv_if_not_exists(self):
        from verifier.classifier_feedback import record_routing_failure
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "nonexistent", "labels.csv")
            record_routing_failure({"prompt": "test", "agreement": 0.1}, labels_csv=csv_path)
            assert os.path.exists(csv_path)
            df = pd.read_csv(csv_path)
            assert len(df) == 1


class TestRerouteHandler:
    @pytest.mark.asyncio
    async def test_reroutes_to_highest_tier(self):
        from verifier.reroute_handler import auto_escalate_and_rerun
        mock_llm = AsyncMock()
        mock_response = type("Resp", (), {"output": "escalated answer", "model_id": "claude-opus-4.6", "success": True})()
        mock_llm.send_request = AsyncMock(return_value=mock_response)

        result = await auto_escalate_and_rerun(
            prompt="test",
            routing_metadata={"model": "gpt-4o-mini"},
            llm=mock_llm,
            logger=None,
        )
        assert result.output == "escalated answer"

    @pytest.mark.asyncio
    async def test_picks_highest_quality_tier_model(self):
        from verifier.reroute_handler import _pick_highest_tier_model
        from models_config import CLAUDE_SONNET_4_6 as ClaudeSonnet46
        model = _pick_highest_tier_model()
        assert model.quality_tier == 10


class TestAsyncVerifier:
    @pytest.mark.asyncio
    async def test_enqueue_and_process(self):
        import asyncio
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()

        mock_result = {"tier": 2, "tier_name": "Tier 2", "confidence": 0.85, "complexity_score": 0.5, "recommended_model_tier": 2}
        pipeline._run_oracle = AsyncMock(return_value=("oracle response", "claude-opus-4.6"))
        pipeline._run_judge = AsyncMock(return_value=(1.0, "perfect match"))
        pipeline._record_failure = AsyncMock()

        await pipeline.enqueue("test prompt", "candidate response", {"model": "gpt-4o-mini", "tier": 1})
        assert pipeline._queue.qsize() == 1

        await pipeline.process_next()
        assert pipeline._queue.qsize() == 0

    @pytest.mark.asyncio
    async def test_agreement_below_threshold_triggers_feedback(self):
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()
        pipeline.AGREEMENT_THRESHOLD = 0.8

        pipeline._run_oracle = AsyncMock(return_value=("oracle", "claude-opus-4.6"))
        pipeline._run_judge = AsyncMock(return_value=(0.3, "poor match"))
        pipeline._record_failure = AsyncMock()
        pipeline._logger = type("MockLogger", (), {"log_verification": lambda *a, **kw: None, "log_rerun": lambda *a, **kw: None})()

        await pipeline.enqueue("prompt", "candidate", {"model": "cheap"})
        await pipeline.process_next()

        pipeline._record_failure.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_high_agreement_skips_feedback(self):
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()

        pipeline._run_oracle = AsyncMock(return_value=("oracle", "claude-opus-4.6"))
        pipeline._run_judge = AsyncMock(return_value=(1.0, "perfect"))
        pipeline._record_failure = AsyncMock()

        await pipeline.enqueue("prompt", "candidate", {"model": "cheap"})
        await pipeline.process_next()

        pipeline._record_failure.assert_not_awaited()

    def test_is_trained_check(self):
        from verifier.async_verifier import VerifierPipeline
        pipeline = VerifierPipeline()
        assert hasattr(pipeline, "_queue")
