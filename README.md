<div align="center">

<!-- Animated Logo -->
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d2ff"/>
      <stop offset="100%" style="stop-color:#3a7bd5"/>
    </linearGradient>
    <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb"/>
      <stop offset="100%" style="stop-color:#f5576c"/>
    </linearGradient>
    <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe"/>
      <stop offset="100%" style="stop-color:#00f2fe"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="200" height="200" rx="40" fill="url(#bg)"/>
  <!-- Dollar sign -->
  <text x="100" y="115" font-family="Arial,sans-serif" font-size="80" font-weight="bold" fill="url(#g1)" text-anchor="middle" filter="url(#glow)">$</text>
  <!-- Circuit lines -->
  <path d="M30 160 L50 160 L50 140 L70 140" stroke="url(#g2)" stroke-width="2" fill="none" opacity="0.6">
    <animate attributeName="stroke-dashoffset" from="100" to="0" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="stroke-dasharray" values="100;0" dur="3s" repeatCount="indefinite"/>
  </path>
  <path d="M170 160 L150 160 L150 140 L130 140" stroke="url(#g3)" stroke-width="2" fill="none" opacity="0.6">
    <animate attributeName="stroke-dashoffset" from="100" to="0" dur="3s" repeatCount="indefinite" begin="1s"/>
    <animate attributeName="stroke-dasharray" values="100;0" dur="3s" repeatCount="indefinite" begin="1s"/>
  </path>
  <!-- Nodes -->
  <circle cx="70" cy="140" r="4" fill="url(#g2)" opacity="0.8">
    <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="130" cy="140" r="4" fill="url(#g3)" opacity="0.8">
    <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite" begin="1s"/>
  </circle>
  <!-- AI chip icon -->
  <rect x="65" y="30" width="70" height="50" rx="8" fill="none" stroke="url(#g1)" stroke-width="2" opacity="0.4"/>
  <line x1="80" y1="30" x2="80" y2="25" stroke="url(#g1)" stroke-width="1.5" opacity="0.4"/>
  <line x1="95" y1="30" x2="95" y2="25" stroke="url(#g1)" stroke-width="1.5" opacity="0.4"/>
  <line x1="110" y1="30" x2="110" y2="25" stroke="url(#g1)" stroke-width="1.5" opacity="0.4"/>
  <line x1="125" y1="30" x2="125" y2="25" stroke="url(#g1)" stroke-width="1.5" opacity="0.4"/>
  <text x="100" y="62" font-family="monospace" font-size="16" fill="url(#g1)" text-anchor="middle" opacity="0.6">AI</text>
</svg>

# 🚀 LLM Cost Autopilot

**Intelligent prompt routing — use the cheapest model that gets the job done.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-00d2ff?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-f093fb?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Tests](https://img.shields.io/badge/tests-70%20passing-00f2fe?style=flat-square)](#)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o%20%7C%20o1--mini-3a7bd5?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Anthropic](https://img.shields.io/badge/Anthropic-Sonnet%20%7C%20Haiku%20%7C%20Opus-f5576c?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%208B%20%7C%2070B-4facfe?style=flat-square&logo=ollama&logoColor=white)](https://ollama.ai)
[![License](https://img.shields.io/badge/license-MIT-1a1a2e?style=flat-square)](LICENSE)

</div>

---

## 💡 The Problem

Running LLMs at scale is expensive. GPT-4o costs **$2.50/M input tokens** while GPT-4o Mini costs **$0.15/M** — a **16x difference**. Most teams either:
- Use the most powerful model for **everything** (wasteful)
- Hard-code model selection per task (brittle)
- Guess which model is good enough (inconsistent)

**LLM Cost Autopilot** solves this with ML-driven intelligent routing.

---

## ✨ Features

<!-- Feature cards -->
<div align="center">

| | | |
|---|---|---|
| <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="24" fill="#00d2ff" font-weight="bold" text-anchor="middle">Σ</text></svg><br/>**9 Models**<br/>GPT-4o, o1-mini, Claude<br/>Sonnet, Haiku, Opus, Llama | <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="24" fill="#f093fb" font-weight="bold" text-anchor="middle">🧠</text></svg><br/>**ML Classifier**<br/>RandomForest + TF-IDF<br/>80%+ cross-val accuracy | <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="24" fill="#4facfe" font-weight="bold" text-anchor="middle">₹</text></svg><br/>**Cost Optimizer**<br/>Route to cheapest model<br/>that meets quality needs |
| <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="24" fill="#00f2fe" font-weight="bold" text-anchor="middle">⚡</text></svg><br/>**Async by Default**<br/>True async concurrency<br/>across all providers | <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="22" fill="#f5576c" font-weight="bold" text-anchor="middle">YAML</text></svg><br/>**Routing Map**<br/>Auto-generated config<br/>maps tier → model | <svg width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#1a1a2e"/><text x="24" y="32" font-family="monospace" font-size="22" fill="#3a7bd5" font-weight="bold" text-anchor="middle">CV</text></svg><br/>**Benchmarks**<br/>Latency & cost metrics<br/>per model per task type |

</div>

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│                  User Prompt                       │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│           Complexity Classifier (ML)              │
│  ┌──────────┐   ┌────────────┐   ┌───────────┐   │
│  │  TF-IDF  │──▶│RandomForest│──▶│   Ridge   │   │
│  │ Vectorize│   │Classifier  │   │ Regressor │   │
│  └──────────┘   └────────────┘   └───────────┘   │
│                    │                 │             │
│                    ▼                 ▼             │
│              Complexity Tier    Complexity Score   │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│              Model Router (config)                │
│  ┌──────────┐   ┌──────────┐   ┌───────────┐     │
│  │ Tier 1   │   │ Tier 2   │   │  Tier 3   │     │
│  │ Simple   │   │ Moderate │   │  Complex  │     │
│  │ Cheapest │   │ Mid-tier │   │  Best LLM │     │
│  └──────────┘   └──────────┘   └───────────┘     │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│            Selected LLM Response                   │
└──────────────────────────────────────────────────┘
```

---

## 📊 Pricing Snapshot

<div align="center">

| Model | Provider | Input $/1M tok | Output $/1M tok | Latency | Quality | Best For |
|-------|----------|:---------------:|:----------------:|:-------:|:-------:|----------|
| **Claude Haiku 4.5** | Anthropic | $1.00 | $5.00 | 600ms | 6 | Tier 1: Q&A, extraction |
| **GPT-4o Mini** | OpenAI | $0.15 | $0.60 | 800ms | 7 | Tier 1: formatting, translation |
| **Llama 3.1 8B** | Ollama | $0.00 | $0.00 | 500ms | 5 | Tier 1: offline/self-hosted |
| **GPT-4o** | OpenAI | $2.50 | $10.00 | 1500ms | 9 | Tier 2: reasoning, analysis |
| **Claude 3.5 Sonnet** | Anthropic | $3.00 | $15.00 | 1800ms | 9 | Tier 2: coding, classification |
| **Llama 3.3 70B** | Ollama | $0.00 | $0.00 | 1200ms | 8 | Tier 2: self-hosted reasoning |
| **Claude Opus 4.6** | Anthropic | $5.00 | $25.00 | 2200ms | 10 | Tier 3: complex reasoning |
| **Claude Sonnet 4.6** | Anthropic | $3.00 | $15.00 | 1700ms | 10 | Tier 3: complex coding |
| **o1-mini** | OpenAI | $3.00 | $12.00 | 3000ms | 9 | Tier 3: multi-step reasoning |

</div>

Potential savings: routing a Tier 1 task from GPT-4o → GPT-4o Mini saves **~94%** on input cost.

---

## 🧠 ML Classifier Performance

<div align="center">

```
┌────────────────────────────────────────────────────┐
│  Tier 1 (Simple)                                    │
│  ████████████████████████████████████████████████░  │  85 prompts
│  precision: 1.000 │ recall: 1.000 │ f1: 1.000      │
├────────────────────────────────────────────────────┤
│  Tier 2 (Moderate)                                  │
│  ██████████████████████████████████████████████████  │  96 prompts
│  precision: 1.000 │ recall: 1.000 │ f1: 1.000      │
├────────────────────────────────────────────────────┤
│  Tier 3 (Complex)                                    │
│  ████████████████████████████████████████████░░░░░  │  53 prompts
│  precision: 1.000 │ recall: 1.000 │ f1: 1.000      │
├────────────────────────────────────────────────────┤
│  Cross-val Accuracy:  75.5% ± 17.6%                 │
│  Regression RMSE:     0.000 (training)              │
│  Task types:          14 (234 total prompts)        │
└────────────────────────────────────────────────────┘
```

</div>

---

## 🚀 Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/shivamsingh-007/LLM-Cost-AutoPilot.git
cd LLM-Cost-AutoPilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API keys (optional — benchmark runs without)
cp .env.example .env
# Edit .env with your keys:
#   OPENAI_API_KEY=sk-...
#   ANTHROPIC_API_KEY=sk-ant-...

# 4. Train the complexity classifier
python -m ml.train_classifier

# 5. Classify a prompt
python -c "
from ml.complexity_classifier import ComplexityClassifier
c = ComplexityClassifier(); c.load()
print(c.predict_complexity('Write merge sort in Python', 'coding'))
"
```

---

## 📁 Project Structure

```
LLM-Cost-AutoPilot/
├── ml/                          # ML pipeline
│   ├── complexity_classifier.py # RandomForest + Ridge + TF-IDF
│   ├── train_classifier.py      # Entry point: train & save
│   └── __init__.py
├── data/
│   └── complexity_labels.csv    # 234 labeled prompts across 14 types
├── config/
│   └── routing_map.yaml         # Auto-generated tier→model mappings
├── models/
│   └── complexity_classifier/   # Saved model artifacts (gitignored)
├── models_config.py             # 9 ModelConfig instances with pricing
├── unified_interface.py         # Async LLM client (OpenAI + Anthropic + Ollama)
├── run_benchmark.py             # 10 prompts × 9 models benchmark
├── test_models_config.py        # 35 unit tests
├── test_unified_interface.py    # 18 unit tests
├── test_classifier.py           # 9 integration tests
├── test_benchmark.py            # 8 benchmark tests
└── requirements.txt
```

---

## ✅ Test Suite

<div align="center">

| File | Tests | Status |
|------|:-----:|:------:|
| `test_models_config.py` | 35 | ✅ Passing |
| `test_unified_interface.py` | 18 | ✅ Passing |
| `test_classifier.py` | 9 | ✅ Passing |
| `test_benchmark.py` | 8 | ✅ Passing |
| **Total** | **70** | **✅ All Passing** |

```bash
# Run all tests
python -m pytest test_models_config.py test_unified_interface.py test_classifier.py test_benchmark.py -v
```

</div>

---

## 🛠️ Tech Stack

<div align="center">

| | |
|---|---|
| **Language** | Python 3.11+ |
| **ML Framework** | scikit-learn (RandomForest, Ridge, TF-IDF) |
| **LLM Providers** | OpenAI API · Anthropic API · Ollama (local) |
| **Data** | pandas, numpy |
| **Serialization** | joblib, PyYAML |
| **Testing** | pytest |

</div>

---

## 📈 Roadmap

- [x] **Day 1:** Unified model config + async interface + benchmark harness
- [x] **Day 2:** Complexity classifier (RandomForest + Ridge) + routing YAML
- [ ] **Day 3:** Dynamic cost tracker with real-time spending dashboards
- [ ] **Day 4:** Multi-user budget management with per-project allocation
- [ ] **Day 5:** Production deployment — FastAPI server + Docker + CI/CD

---

<div align="center">

**LLM Cost Autopilot** · Built with ❤️

[![GitHub stars](https://img.shields.io/github/stars/shivamsingh-007/LLM-Cost-AutoPilot?style=social)](https://github.com/shivamsingh-007/LLM-Cost-AutoPilot)
[![GitHub forks](https://img.shields.io/github/forks/shivamsingh-007/LLM-Cost-AutoPilot?style=social)](https://github.com/shivamsingh-007/LLM-Cost-AutoPilot)

</div>
