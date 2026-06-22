from __future__ import annotations

import csv
import io
import tempfile
from pathlib import Path

from run_benchmark import BenchmarkPrompt, PROMPTS, save_csv


class TestPromptStructure:
    def test_has_ten_prompts(self):
        assert len(PROMPTS) == 10

    def test_each_prompt_has_required_fields(self):
        for p in PROMPTS:
            assert isinstance(p, BenchmarkPrompt)
            assert p.prompt_id
            assert p.prompt_name
            assert p.prompt_text
            assert isinstance(p.complexity, float)
            assert 0.0 <= p.complexity <= 1.0

    def test_unique_ids(self):
        ids = [p.prompt_id for p in PROMPTS]
        assert len(ids) == len(set(ids))

    def test_complexity_values(self):
        expected = {0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
        actual = {p.complexity for p in PROMPTS}
        assert actual == expected, f"Missing complexity values: {expected - actual}"

    def test_system_prompt_some_empty(self):
        has_system = sum(1 for p in PROMPTS if p.system_prompt)
        assert 0 < has_system < 10, "Some prompts should have system prompts, some not"


class TestSaveCsv:
    def test_writes_expected_columns(self):
        rows = [
            {
                "model": "GPT-4o",
                "prompt_id": "P01",
                "prompt_name": "Simple Query",
                "complexity": 0.2,
                "success": True,
                "latency_ms": 1500.0,
                "cost_usd": 0.000025,
                "tokens_total": 50,
                "output_length": 20,
                "error": "",
            }
        ]
        buf = io.StringIO()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            save_csv(rows, f.name)
            f.flush()
            content = Path(f.name).read_text(encoding="utf-8")
        Path(f.name).unlink()

        reader = csv.DictReader(io.StringIO(content))
        assert reader.fieldnames == [
            "model", "prompt_id", "prompt_name", "complexity", "success",
            "latency_ms", "cost_usd", "tokens_total", "output_length", "error",
        ]

    def test_output_column_not_in_csv(self):
        rows = [
            {
                "model": "GPT-4o",
                "prompt_id": "P01",
                "prompt_name": "Simple Query",
                "complexity": 0.2,
                "success": True,
                "latency_ms": 1500.0,
                "cost_usd": 0.000025,
                "tokens_total": 50,
                "output_length": 20,
                "error": "",
                "_output": "Paris",
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            save_csv(rows, f.name)
            f.flush()
            content = Path(f.name).read_text(encoding="utf-8")
        Path(f.name).unlink()

        reader = csv.DictReader(io.StringIO(content))
        assert "output" not in reader.fieldnames
        assert "model" in reader.fieldnames
        assert "prompt_id" in reader.fieldnames

    def test_multiple_rows(self):
        rows = [
            {
                "model": "GPT-4o",
                "prompt_id": f"P{i:02d}",
                "prompt_name": f"Prompt {i}",
                "complexity": 0.5,
                "success": True,
                "latency_ms": 1000.0,
                "cost_usd": 0.001,
                "tokens_total": 100,
                "output_length": 50,
                "error": "",
            }
            for i in range(1, 4)
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            save_csv(rows, f.name)
            f.flush()
            content = Path(f.name).read_text(encoding="utf-8")
        Path(f.name).unlink()

        lines = content.strip().split("\n")
        assert len(lines) == 4  # header + 3 rows
