from __future__ import annotations

import os
from typing import Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
import scipy.sparse
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import classification_report, mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


class ComplexityClassifier:
    MODELS_DIR = "models/complexity_classifier"
    TIER_BOUNDARIES = [(0.0, 0.35), (0.36, 0.65), (0.66, 1.0)]
    TIER_NAMES = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3"}
    TIER_LABELS = {1: "simple", 2: "moderate", 3: "complex"}

    _TASK_MAP = {
        "extraction": "simple fact retrieval",
        "qa": "simple fact retrieval",
        "translation": "simple transformation",
        "formatting": "simple transformation",
        "summarization": "moderate analysis",
        "classification": "moderate analysis",
        "explanation": "moderate reasoning",
        "analysis": "moderate analysis",
        "rewriting": "moderate transformation",
        "coding": "complex coding",
        "reasoning": "complex reasoning",
        "creative": "complex creative",
        "planning": "complex planning",
        "math": "complex reasoning",
    }

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42)
        self.regressor = make_pipeline(StandardScaler(with_mean=False), Ridge(alpha=1.0))
        self._is_trained = False

    def _encode_task_type(self, task_types: List[str]) -> List[str]:
        return [self._TASK_MAP.get(t, "unknown") for t in task_types]

    def _build_features(self, prompts: List[str], task_types: List[str]) -> np.ndarray:
        text_features = self.vectorizer.transform(prompts)
        encoded = self._encode_task_type(task_types)
        type_features = self.vectorizer.transform(encoded)
        return scipy.sparse.hstack([text_features, type_features])

    def train(self, dataframe: pd.DataFrame) -> Dict:
        df = dataframe.dropna(subset=["prompt", "complexity_tier"])
        prompts = df["prompt"].tolist()
        task_types = df.get("task_type", ["unknown"] * len(prompts)).fillna("unknown").tolist()
        tiers = df["complexity_tier"].values
        scores = df.get("complexity_score", np.zeros(len(prompts))).values

        X_tfidf = self.vectorizer.fit_transform(prompts)
        encoded = self._encode_task_type(task_types)
        type_features = self.vectorizer.transform(encoded)
        X = scipy.sparse.hstack([X_tfidf, type_features])

        self.classifier.fit(X, tiers)
        self.regressor.fit(X, scores)

        cv_scores = cross_val_score(self.classifier, X, tiers, cv=5)
        preds = self.classifier.predict(X)
        report = classification_report(tiers, preds, output_dict=True)
        train_scores = self.regressor.predict(X)
        rmse = np.sqrt(mean_squared_error(scores, train_scores))

        self._is_trained = True

        return {
            "accuracy": float((preds == tiers).mean()),
            "cv_mean": float(cv_scores.mean()),
            "cv_std": float(cv_scores.std()),
            "classification_report": report,
            "rmse": float(rmse),
        }

    def predict_complexity(self, prompt: str, task_type: Optional[str] = None) -> Dict:
        if not self._is_trained:
            raise RuntimeError("Model not trained. Call train() or load() first.")

        task_type = task_type or "unknown"
        features = self._build_features([prompt], [task_type])
        tier = int(self.classifier.predict(features)[0])
        probs = self.classifier.predict_proba(features)[0]
        confidence = float(max(probs))
        score = float(self.regressor.predict(features)[0])
        score = max(0.0, min(1.0, score))

        return {
            "tier": tier,
            "tier_name": self.TIER_NAMES[tier],
            "confidence": round(confidence, 3),
            "complexity_score": round(score, 3),
            "recommended_model_tier": tier,
        }

    def load(self) -> bool:
        try:
            self.vectorizer = joblib.load(os.path.join(self.MODELS_DIR, "vectorizer.joblib"))
            self.classifier = joblib.load(os.path.join(self.MODELS_DIR, "classifier.joblib"))
            self.regressor = joblib.load(os.path.join(self.MODELS_DIR, "regressor.joblib"))
            self._is_trained = True
            return True
        except (FileNotFoundError, OSError):
            return False

    def save(self):
        os.makedirs(self.MODELS_DIR, exist_ok=True)
        joblib.dump(self.vectorizer, os.path.join(self.MODELS_DIR, "vectorizer.joblib"))
        joblib.dump(self.classifier, os.path.join(self.MODELS_DIR, "classifier.joblib"))
        joblib.dump(self.regressor, os.path.join(self.MODELS_DIR, "regressor.joblib"))

    def generate_routing_map(self, output_path: str = "config/routing_map.yaml"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        routing = {
            "version": 1,
            "description": "Prompt complexity routing map — auto-generated from classifier training",
            "tiers": [
                {
                    "tier": 1,
                    "name": "simple",
                    "range": [0.0, 0.35],
                    "use_cases": ["extraction", "qa", "translation", "formatting"],
                    "recommended_models": ["claude-haiku-4.5", "gpt-4o-mini", "llama3.1-8b"],
                    "fallback_model": "gpt-4o-mini",
                },
                {
                    "tier": 2,
                    "name": "moderate",
                    "range": [0.36, 0.65],
                    "use_cases": ["summarization", "classification", "explanation", "analysis", "rewriting"],
                    "recommended_models": ["gpt-4o", "claude-3.5-sonnet", "llama3.3-70b"],
                    "fallback_model": "gpt-4o",
                },
                {
                    "tier": 3,
                    "name": "complex",
                    "range": [0.66, 1.0],
                    "use_cases": ["coding", "reasoning", "creative", "planning", "math"],
                    "recommended_models": ["claude-opus-4.6", "claude-sonnet-4.6", "o1-mini"],
                    "fallback_model": "claude-sonnet-4.6",
                },
            ],
        }
        with open(output_path, "w") as f:
            yaml.dump(routing, f, default_flow_style=False, sort_keys=False)

    @property
    def is_trained(self) -> bool:
        return self._is_trained
