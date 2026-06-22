from __future__ import annotations

import pandas as pd

from ml.complexity_classifier import ComplexityClassifier


def main():
    print("Loading labeled prompts...")
    df = pd.read_csv("data/complexity_labels.csv")
    print(f"  Loaded {len(df)} prompts")
    print(f"  Tier distribution:\n{df['complexity_tier'].value_counts().sort_index().to_string()}")

    print("\nTraining classifier and regressor...")
    clf = ComplexityClassifier()
    metrics = clf.train(df)

    print(f"\n  Accuracy: {metrics['accuracy']:.3f}")
    print(f"  Cross-val accuracy: {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
    print(f"  Regression RMSE: {metrics['rmse']:.3f}")

    print("\n  Per-tier F1:")
    for tier_label in ["1", "2", "3"]:
        if tier_label in metrics["classification_report"]:
            info = metrics["classification_report"][tier_label]
            print(f"    Tier {tier_label}: precision={info['precision']:.3f} "
                  f"recall={info['recall']:.3f} f1={info['f1-score']:.3f} "
                  f"support={int(info['support'])}")

    clf.save()
    print(f"\nModel artifacts saved to {clf.MODELS_DIR}/")

    clf.generate_routing_map()
    print("Routing map saved to config/routing_map.yaml")

    print("\nSample predictions:")
    samples = [
        ("What is the capital of France?", "qa"),
        ("Summarize this article in 3 sentences", "summarization"),
        ("Write a Python function that implements merge sort", "coding"),
    ]
    for prompt, task_type in samples:
        result = clf.predict_complexity(prompt, task_type)
        print(f"  [{result['tier_name']:>10}] "
              f"(score={result['complexity_score']:.2f}, "
              f"conf={result['confidence']:.2f}) "
              f"{prompt}")


if __name__ == "__main__":
    main()
