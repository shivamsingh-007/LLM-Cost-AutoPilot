from __future__ import annotations

import asyncio
import csv
from dataclasses import dataclass, asdict
from typing import Dict, List

from models_config import ALL_MODELS, GPT4O, ModelConfig
from unified_interface import UnifiedLLMInterface


@dataclass
class BenchmarkPrompt:
    prompt_id: str
    prompt_name: str
    prompt_text: str
    system_prompt: str
    complexity: float


PROMPTS: List[BenchmarkPrompt] = [
    BenchmarkPrompt(
        prompt_id="P01",
        prompt_name="Simple Query",
        prompt_text="What is the capital of France?",
        system_prompt="",
        complexity=0.2,
    ),
    BenchmarkPrompt(
        prompt_id="P02",
        prompt_name="Coding Task",
        prompt_text="Write a Python function to reverse a string without using built-in reverse()",
        system_prompt="You are a Python expert.",
        complexity=0.5,
    ),
    BenchmarkPrompt(
        prompt_id="P03",
        prompt_name="Math Problem",
        prompt_text="If a train travels 120 miles in 2 hours, what is its average speed in mph?",
        system_prompt="",
        complexity=0.6,
    ),
    BenchmarkPrompt(
        prompt_id="P04",
        prompt_name="Creative Writing",
        prompt_text="Write a 100-word story about a robot discovering emotions.",
        system_prompt="",
        complexity=0.4,
    ),
    BenchmarkPrompt(
        prompt_id="P05",
        prompt_name="Analysis",
        prompt_text="Compare machine learning and deep learning. List 3 key differences.",
        system_prompt="Provide a technical comparison.",
        complexity=0.7,
    ),
    BenchmarkPrompt(
        prompt_id="P06",
        prompt_name="Complex Reasoning",
        prompt_text="If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? Explain your reasoning.",
        system_prompt="",
        complexity=0.8,
    ),
    BenchmarkPrompt(
        prompt_id="P07",
        prompt_name="Long Context",
        prompt_text="Summarize the main points of the following text:\n\nArtificial intelligence has evolved rapidly over the past decade, transitioning from narrow AI systems designed for specific tasks to increasingly general-purpose models capable of handling diverse challenges. Early deep learning breakthroughs in image recognition and natural language processing laid the groundwork for transformer architectures, which revolutionized how machines understand and generate human language. The development of large language models trained on vast internet-scale datasets demonstrated emergent abilities in reasoning, translation, and code generation that were not explicitly programmed. These models exhibit in-context learning, allowing them to adapt to new tasks without fine-tuning. However, challenges remain in areas such as factual accuracy, bias mitigation, and alignment with human values. Researchers continue to explore techniques including reinforcement learning from human feedback, retrieval-augmented generation, and chain-of-thought prompting to improve reliability and safety. The field is also seeing increased focus on multimodal models that process text, images, audio, and video simultaneously, as well as agentic systems that can plan and execute complex sequences of actions autonomously.",
        system_prompt="",
        complexity=0.6,
    ),
    BenchmarkPrompt(
        prompt_id="P08",
        prompt_name="JSON Generation",
        prompt_text="Generate JSON with user data: name (string), age (int), is_active (boolean), skills (array of strings)",
        system_prompt="Return only valid JSON.",
        complexity=0.5,
    ),
    BenchmarkPrompt(
        prompt_id="P09",
        prompt_name="Debugging",
        prompt_text="Find the bug: def factorial(n): if n == 0: return 1; else: return n * factorial(n)",
        system_prompt="You are a debugging expert.",
        complexity=0.7,
    ),
    BenchmarkPrompt(
        prompt_id="P10",
        prompt_name="Multi-step Task",
        prompt_text="Plan a 3-day trip to Jaipur. Include: (1) Day-by-day itinerary, (2) Top 3 attractions per day, (3) Estimated budget in INR",
        system_prompt="Be detailed and practical.",
        complexity=0.9,
    ),
]


async def _run_single(
    llm: UnifiedLLMInterface,
    model_config: ModelConfig,
    prompt: BenchmarkPrompt,
) -> Dict:
    resp = await llm.send_request(
        prompt=prompt.prompt_text,
        model_config=model_config,
        system_prompt=prompt.system_prompt,
    )
    tokens_total = resp.tokens.get("input", 0) + resp.tokens.get("output", 0)
    return {
        "model": model_config.display_name,
        "prompt_id": prompt.prompt_id,
        "prompt_name": prompt.prompt_name,
        "complexity": prompt.complexity,
        "success": resp.success,
        "latency_ms": round(resp.latency_ms, 2),
        "cost_usd": round(resp.cost_usd, 6),
        "tokens_total": tokens_total,
        "output_length": len(resp.output) if resp.success else 0,
        "error": resp.error_message,
        "_output": resp.output,
    }


async def run_model_benchmark(
    llm: UnifiedLLMInterface,
    model_config: ModelConfig,
    prompts: List[BenchmarkPrompt],
) -> List[Dict]:
    results = await asyncio.gather(
        *[_run_single(llm, model_config, p) for p in prompts]
    )
    return results


def print_results_line(result: Dict) -> None:
    status = "OK" if result["success"] else "FAIL"
    print(
        f"  {result['prompt_name']:20s} {status:4s}  "
        f"{result['latency_ms']:8.0f}ms  "
        f"${result['cost_usd']:<8.6f}  "
        f"{result['tokens_total']:5d} tok"
    )


def print_summary_table(models_results: Dict[str, List[Dict]]) -> None:
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Model':25s} {'Success':8s} {'Avg Latency':12s} {'Avg Cost':12s} {'Avg Tokens':10s}")
    print("-" * 80)
    for model_name, results in models_results.items():
        total = len(results)
        ok = sum(1 for r in results if r["success"])
        avg_lat = sum(r["latency_ms"] for r in results) / total
        avg_cost = sum(r["cost_usd"] for r in results) / total
        avg_tok = sum(r["tokens_total"] for r in results) / total
        print(
            f"{model_name:25s} {ok:2d}/{total:<2d}  "
            f"{avg_lat:8.0f}ms     "
            f"${avg_cost:<8.6f}  "
            f"{avg_tok:6.0f}"
        )


def print_cost_comparison(models_results: Dict[str, List[Dict]]) -> None:
    print("\n" + "-" * 80)
    print("COST COMPARISON VS GPT-4o BASELINE")
    print("-" * 80)
    baseline_total = sum(r["cost_usd"] for r in models_results.get(GPT4O.display_name, []))
    print(f"{'Model':25s} {'Total Cost':12s} {'Savings':10s}")
    print("-" * 80)
    for model_name, results in models_results.items():
        total_cost = sum(r["cost_usd"] for r in results)
        if baseline_total > 0 and model_name != GPT4O.display_name:
            savings = ((baseline_total - total_cost) / baseline_total) * 100
            print(f"{model_name:25s} ${total_cost:<9.6f}  {savings:>+6.1f}%")
        else:
            print(f"{model_name:25s} ${total_cost:<9.6f}  {'-':>6s}")


def save_csv(all_results: List[Dict], path: str = "test_results.csv") -> None:
    fields = ["model", "prompt_id", "prompt_name", "complexity", "success",
              "latency_ms", "cost_usd", "tokens_total", "output_length", "error"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in all_results:
            writer.writerow({k: r[k] for k in fields})


async def main() -> None:
    llm = UnifiedLLMInterface()

    all_results: List[Dict] = []
    models_results: Dict[str, List[Dict]] = {}

    for model_config in ALL_MODELS:
        name = model_config.display_name
        print(f"\n{'=' * 80}")
        print(f"Model: {name}")
        print(f"{'=' * 80}")

        results = await run_model_benchmark(llm, model_config, PROMPTS)
        models_results[name] = results
        all_results.extend(results)

        for r in results:
            print_results_line(r)

    print_summary_table(models_results)
    print_cost_comparison(models_results)
    save_csv(all_results)

    summary_ok = sum(1 for r in all_results if r["success"])
    summary_total = len(all_results)
    print(f"\n{'=' * 80}")
    print(f"BENCHMARK COMPLETE: {summary_ok}/{summary_total} requests succeeded")
    print(f"Results saved to test_results.csv")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    asyncio.run(main())
