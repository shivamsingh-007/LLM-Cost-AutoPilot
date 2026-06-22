# Spec: Complexity Classifier

## Objective
Train an ML model that predicts the complexity tier (1/2/3) and a continuous complexity score (0–1) for a user prompt. The output feeds a downstream router that assigns the cheapest capable LLM. Tier 1 → cheap model (Haiku, Mini, Llama 8B), Tier 2 → mid (GPT-4o, Sonnet, Llama 70B), Tier 3 → best (Opus, o1-mini, Sonnet 4.6). Also produces a YAML routing map as a standalone artifact.

## Tech Stack
- Python 3.10+, same venv as Day 1
- scikit-learn (RandomForestClassifier + Ridge regressor)
- pandas, numpy, joblib, pyyaml
- TF-IDF vectorizer (unigrams + bigrams, max 5000 features)
- No external ML APIs

## Commands
```
Train:     python ml/train_classifier.py
Test:      python -m pytest test_classifier.py -v
Predict:   python -c "from ml.complexity_classifier import ComplexityClassifier; c=ComplexityClassifier(); c.load(); print(c.predict_complexity('write a function', 'coding'))"
Lint:      ruff check ml/ data/
```

## Project Structure
```
ml/
  complexity_classifier.py   → ComplexityClassifier class (classifier + regressor + routing YAML)
  train_classifier.py        → Training script (entry point)
data/
  complexity_labels.csv      → 220 hand-labeled prompts
models/
  complexity_classifier/     → Saved artifacts (model.joblib, vectorizer.joblib, regressor.joblib)
config/
  routing_map.yaml           → Generated routing map with tiers, model recs, use cases
test_classifier.py           → 6 edge-case integration tests
```

## Code Style

```python
class ComplexityClassifier:
    """Single sentence docstring. Public methods documented."""

    TIER_NAMES = {0: "Tier 1", 1: "Tier 2", 2: "Tier 3"}

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42)
        self.regressor = Ridge(alpha=1.0)  # predicts continuous 0-1 score
```

- Classes: PascalCase
- Functions/methods: snake_case
- Constants: UPPER_SNAKE_CASE
- Private methods prefixed `_`
- Imports: stdlib → third-party → local, one blank line between groups

## Testing Strategy

| Level | File | What |
|-------|------|------|
| Unit | `test_classifier.py` | 6 hand-picked prompts, verify tier matches expectation, score is 0-1 |
| Training | `ml/train_classifier.py` | Prints accuracy, CV score, classification report. Not automated CI (depends on CSV data) |

Accuracy target: 80%+ on held-out test set (stratified 80/20 split). Regression target: RMSE < 0.15 on held-out scores.

## Boundaries

- **Always:** Save model artifacts after training, print accuracy + CV score, write regression test for each of the 3 tiers
- **Ask first:** Changing the model family (e.g., RandomForest → XGBoost), adding new features beyond TF-IDF + task_type, changing tier boundary thresholds
- **Never:** Commit `models/` binary artifacts larger than 10MB, hardcode API keys in training scripts, delete labeled data

## Success Criteria

1. `python ml/train_classifier.py` completes with accuracy ≥ 80%, no errors
2. Classification report shows ≥ 75% F1 per tier
3. Regression model predicts scores within (0, 1) range, RMSE < 0.15
4. `config/routing_map.yaml` generated with correct model recs for all 3 tiers
5. `test_classifier.py` passes 6/6 tests (one per tier type)
6. `predict_complexity("write a function", "coding")` returns dict with `tier`, `confidence`, `complexity_score`, `recommended_model_tier`

## Open Questions

None — spec covers labeled data, dual model (classifier + regressor), YAML output, and test cases as discussed.
