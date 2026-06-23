from __future__ import annotations

import os
import tempfile

import numpy as np
import pandas as pd
import pytest
import yaml

from ml.complexity_classifier import ComplexityClassifier


@pytest.fixture
def trained_clf():
    df = pd.read_csv("data/complexity_labels.csv")
    clf = ComplexityClassifier()
    clf.train(df)
    return clf


class TestTraining:
    def test_accuracy_above_threshold(self, trained_clf):
        df = pd.read_csv("data/complexity_labels.csv")
        metrics = trained_clf.train(df)
        assert metrics["cv_mean"] >= 0.70

    def test_save_and_load(self, trained_clf):
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = ComplexityClassifier.MODELS_DIR
            ComplexityClassifier.MODELS_DIR = tmpdir
            try:
                trained_clf.save()
                loaded = ComplexityClassifier()
                assert loaded.load()
                assert loaded.is_trained
            finally:
                ComplexityClassifier.MODELS_DIR = original_dir


class TestPrediction:
    def test_simple_qa_returns_tier1(self, trained_clf):
        result = trained_clf.predict_complexity("What is the capital of France?", "qa")
        assert result["tier"] == 1
        assert result["complexity_score"] <= 0.4
        assert result["confidence"] > 0.3

    def test_moderate_summarization_returns_reasonable_tier(self, trained_clf):
        result = trained_clf.predict_complexity("Summarize this article in 3 sentences", "summarization")
        assert result["tier"] in (1, 2)
        assert result["confidence"] > 0.3

    def test_complex_coding_returns_reasonable_tier(self, trained_clf):
        result = trained_clf.predict_complexity("Write a Python function that implements merge sort", "coding")
        assert result["tier"] in (2, 3)

    def test_return_structure(self, trained_clf):
        result = trained_clf.predict_complexity("test prompt", "qa")
        assert set(result.keys()) == {"tier", "tier_name", "confidence", "complexity_score", "recommended_model_tier"}
        assert isinstance(result["tier"], int)
        assert isinstance(result["confidence"], float)
        assert isinstance(result["complexity_score"], float)

    def test_unprompted_task_type_defaults_to_unknown(self, trained_clf):
        result = trained_clf.predict_complexity("What is 2+2?")
        assert isinstance(result["tier"], int)
        assert 0.0 <= result["complexity_score"] <= 1.0

    def test_score_always_in_range(self, trained_clf):
        for prompt in ["Hello world", "Explain quantum computing", "Design a distributed system"]:
            result = trained_clf.predict_complexity(prompt)
            assert 0.0 <= result["complexity_score"] <= 1.0


class TestRoutingMap:
    def test_generates_valid_yaml(self, trained_clf):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "routing_map.yaml")
            trained_clf.generate_routing_map(path)
            with open(path) as f:
                data = yaml.safe_load(f)
            assert data["version"] == 1
            assert len(data["tiers"]) == 3
            for tier in data["tiers"]:
                assert "tier" in tier
                assert "recommended_models" in tier
                assert "fallback_model" in tier
