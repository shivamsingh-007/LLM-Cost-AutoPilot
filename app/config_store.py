from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path("config/routing_runtime.json")


class RoutingConfigStore:
    def __init__(self):
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not CONFIG_PATH.exists():
            self._write({
                "routing_mode": "balanced",
                "complexity_threshold_simple": 0.35,
                "complexity_threshold_medium": 0.65,
                "min_quality_score": 0.75,
                "rules": [],
            })

    def _read(self):
        return json.loads(CONFIG_PATH.read_text())

    def _write(self, data):
        CONFIG_PATH.write_text(json.dumps(data, indent=2))

    def get(self):
        return self._read()

    def update(self, patch):
        current = self._read()
        for k, v in patch.items():
            if v is not None:
                current[k] = v
        self._write(current)
        return current
