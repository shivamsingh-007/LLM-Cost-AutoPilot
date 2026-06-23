from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    ENABLE_LANGFUSE: bool = False
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""

    def __init__(self):
        self.ENABLE_LANGFUSE = os.getenv("ENABLE_LANGFUSE", "").lower() == "true"
        self.LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        self.LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")


settings = Settings()
