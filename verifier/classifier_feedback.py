from __future__ import annotations

import os

import pandas as pd


def record_routing_failure(failure_record: dict, labels_csv: str = "data/complexity_labels.csv"):
    prompt = failure_record.get("prompt", "")
    agreement = failure_record.get("agreement", 0.0)

    os.makedirs(os.path.dirname(labels_csv) or ".", exist_ok=True)

    new_row = {
        "prompt": prompt.replace("\n", " "),
        "task_type": "verifier_failure",
        "complexity_score": round(max(0.0, min(1.0, 1.0 - agreement)), 3),
        "complexity_tier": 3,
    }

    if os.path.exists(labels_csv):
        df = pd.read_csv(labels_csv)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(labels_csv, index=False)
