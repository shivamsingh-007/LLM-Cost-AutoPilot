from __future__ import annotations

from typing import Any, Dict, Optional

from config.settings import settings


class LangfuseLogger:
    def __init__(self):
        self._lf = None
        if settings.ENABLE_LANGFUSE and settings.LANGFUSE_SECRET_KEY:
            try:
                from langfuse import Langfuse as _Langfuse
                self._lf = _Langfuse(
                    public_key=settings.LANGFUSE_PUBLIC_KEY,
                    secret_key=settings.LANGFUSE_SECRET_KEY,
                )
            except ImportError:
                pass

    def log_verification(self, **kwargs):
        if self._lf is None:
            return
        trace = self._lf.trace(name="verification", input=kwargs.get("prompt"))
        trace.metadata(kwargs)
        score = kwargs.get("agreement")
        if score is not None:
            trace.score(name="agreement", value=score)
        trace.flush()

    def log_rerun(self, **kwargs):
        if self._lf is None:
            return
        trace = self._lf.trace(name="escalation", input=kwargs.get("original_response"))
        trace.metadata(kwargs)
        trace.flush()

    def log_error(self, tag: str, data: Dict[str, Any]):
        if self._lf is None:
            return
        trace = self._lf.trace(name="error", input=tag)
        trace.metadata(data)
        trace.flush()
