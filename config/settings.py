from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    def __init__(self):
        self.ENABLE_LANGFUSE = os.getenv("ENABLE_LANGFUSE", "").lower() == "true"
        self.LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        self.LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
        self.ROUTING_MODE = os.getenv("ROUTING_MODE", "balanced")
        self.COMPLEXITY_THRESHOLD_SIMPLE = float(os.getenv("COMPLEXITY_THRESHOLD_SIMPLE", "0.35"))
        self.COMPLEXITY_THRESHOLD_MEDIUM = float(os.getenv("COMPLEXITY_THRESHOLD_MEDIUM", "0.65"))
        self.MIN_QUALITY_SCORE = float(os.getenv("MIN_QUALITY_SCORE", "0.75"))


settings = Settings()
