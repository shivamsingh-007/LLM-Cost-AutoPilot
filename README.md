<div align="center">

<!-- ─── ANIMATED LOGO ─── -->
<svg width="280" height="280" viewBox="0 0 280 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f0c29"/><stop offset="50%" stop-color="#302b63"/><stop offset="100%" stop-color="#24243e"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00d2ff"/><stop offset="100%" stop-color="#3a7bd5"/>
    </linearGradient>
    <linearGradient id="pinkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f093fb"/><stop offset="100%" stop-color="#f5576c"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#43e97b"/><stop offset="100%" stop-color="#38f9d7"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f6d365"/><stop offset="100%" stop-color="#fda085"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="softGlow"><feGaussianBlur stdDeviation="6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Background -->
  <rect width="280" height="280" rx="48" fill="url(#bgGrad)"/>
  <!-- Orbiting ring -->
  <ellipse cx="140" cy="140" rx="110" ry="110" fill="none" stroke="rgba(0,210,255,0.12)" stroke-width="1">
    <animateTransform attributeName="transform" type="rotate" from="0 140 140" to="360 140 140" dur="20s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="140" cy="140" rx="90" ry="90" fill="none" stroke="rgba(240,147,251,0.08)" stroke-width="0.8">
    <animateTransform attributeName="transform" type="rotate" from="360 140 140" to="0 140 140" dur="15s" repeatCount="indefinite"/>
  </ellipse>
  <!-- Outer nodes on ring -->
  <circle r="4" fill="url(#cyanGrad)" opacity="0.7">
    <animateMotion dur="20s" repeatCount="indefinite" path="M140,30 A110,110 0 1,1 139.9,30"/>
  </circle>
  <circle r="3" fill="url(#pinkGrad)" opacity="0.5">
    <animateMotion dur="15s" repeatCount="indefinite" path="M140,50 A90,90 0 1,0 139.9,50"/>
  </circle>
  <!-- Dollar sign -->
  <text x="140" y="155" font-family="'Segoe UI',Arial,sans-serif" font-size="90" font-weight="900" fill="url(#cyanGrad)" text-anchor="middle" filter="url(#glow)">$</text>
  <!-- Circuit paths -->
  <path d="M50 200 L70 200 L70 180 L90 180" stroke="url(#pinkGrad)" stroke-width="2" fill="none" opacity="0.5">
    <animate attributeName="stroke-dashoffset" from="100" to="0" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="stroke-dasharray" values="100;0" dur="3s" repeatCount="indefinite"/>
  </path>
  <path d="M230 200 L210 200 L210 180 L190 180" stroke="url(#greenGrad)" stroke-width="2" fill="none" opacity="0.5">
    <animate attributeName="stroke-dashoffset" from="100" to="0" dur="3s" repeatCount="indefinite" begin="1s"/>
    <animate attributeName="stroke-dasharray" values="100;0" dur="3s" repeatCount="indefinite" begin="1s"/>
  </path>
  <!-- Nodes on circuits -->
  <circle cx="90" cy="180" r="5" fill="url(#pinkGrad)" opacity="0.8">
    <animate attributeName="r" values="5;7;5" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="190" cy="180" r="5" fill="url(#greenGrad)" opacity="0.8">
    <animate attributeName="r" values="5;7;5" dur="2s" repeatCount="indefinite" begin="1s"/>
  </circle>
  <!-- AI processor at top -->
  <rect x="105" y="30" width="70" height="50" rx="10" fill="none" stroke="url(#cyanGrad)" stroke-width="1.5" opacity="0.3"/>
  <line x1="120" y1="30" x2="120" y2="24" stroke="url(#cyanGrad)" stroke-width="1.5" opacity="0.3"/>
  <line x1="140" y1="30" x2="140" y2="24" stroke="url(#cyanGrad)" stroke-width="1.5" opacity="0.3"/>
  <line x1="160" y1="30" x2="160" y2="24" stroke="url(#cyanGrad)" stroke-width="1.5" opacity="0.3"/>
  <text x="140" y="62" font-family="monospace" font-size="18" fill="url(#cyanGrad)" text-anchor="middle" opacity="0.5" font-weight="bold">AI</text>
  <!-- Small label -->
  <text x="140" y="225" font-family="'Segoe UI',Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.25)" text-anchor="middle" letter-spacing="3">COST AUTOPILOT</text>
</svg>

# LLM Cost Autopilot

**I built an LLM cost autopilot that dynamically routes requests to cheaper models, cutting API spend by 92% while preserving 85% of baseline quality.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-00d2ff?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-f093fb?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-43e97b?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.0%2B-fff000?style=flat-square&logo=duckdb&logoColor=black)](https://duckdb.org)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ed?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Tests](https://img.shields.io/badge/tests-96%20passing-38f9d7?style=flat-square)](#)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o%20%7C%20o1--mini-3a7bd5?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Anthropic](https://img.shields.io/badge/Anthropic-Sonnet%20%7C%20Haiku%20%7C%20Opus-f5576c?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%208B%20%7C%2070B-4facfe?style=flat-square&logo=ollama&logoColor=white)](https://ollama.ai)
[![License](https://img.shields.io/badge/license-MIT-0f0c29?style=flat-square)](LICENSE)

</div>

---

## 📈 Portfolio Report

<div align="center">

<!-- Metric Cards SVG -->
<svg width="760" height="130" viewBox="0 0 760 130" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="c1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00d2ff"/><stop offset="100%" stop-color="#3a7bd5"/>
    </linearGradient>
    <linearGradient id="c2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#43e97b"/><stop offset="100%" stop-color="#38f9d7"/>
    </linearGradient>
    <linearGradient id="c3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f093fb"/><stop offset="100%" stop-color="#f5576c"/>
    </linearGradient>
    <linearGradient id="c4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f6d365"/><stop offset="100%" stop-color="#fda085"/>
    </linearGradient>
    <filter id="cardShadow"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.3)"/></filter>
  </defs>
  <!-- Card 1 -->
  <rect x="10" y="10" width="175" height="110" rx="16" fill="#1a1a2e" filter="url(#cardShadow)"/>
  <text x="97" y="45" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="url(#c1)" text-anchor="middle">740</text>
  <text x="97" y="65" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)" text-anchor="middle">PROMPTS TESTED</text>
  <rect x="30" y="75" width="135" height="3" rx="1.5" fill="url(#c1)" opacity="0.3"/>
  <text x="97" y="100" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.35)" text-anchor="middle">234 labeled + 506 synthetic</text>
  <!-- Card 2 -->
  <rect x="195" y="10" width="175" height="110" rx="16" fill="#1a1a2e" filter="url(#cardShadow)"/>
  <text x="282" y="45" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="url(#c2)" text-anchor="middle">92.3%</text>
  <text x="282" y="65" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)" text-anchor="middle">COST REDUCTION</text>
  <rect x="215" y="75" width="135" height="3" rx="1.5" fill="url(#c2)" opacity="0.3"/>
  <text x="282" y="100" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.35)" text-anchor="middle">$0.020 routed vs $0.264 baseline</text>
  <!-- Card 3 -->
  <rect x="380" y="10" width="175" height="110" rx="16" fill="#1a1a2e" filter="url(#cardShadow)"/>
  <text x="467" y="45" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="url(#c3)" text-anchor="middle">85.4%</text>
  <text x="467" y="65" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)" text-anchor="middle">QUALITY PARITY</text>
  <rect x="400" y="75" width="135" height="3" rx="1.5" fill="url(#c3)" opacity="0.3"/>
  <text x="467" y="100" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.35)" text-anchor="middle">Avg quality score: 0.854 / 1.0</text>
  <!-- Card 4 -->
  <rect x="565" y="10" width="175" height="110" rx="16" fill="#1a1a2e" filter="url(#cardShadow)"/>
  <text x="652" y="45" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="url(#c4)" text-anchor="middle">17.4%</text>
  <text x="652" y="65" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)" text-anchor="middle">ESCALATION RATE</text>
  <rect x="585" y="75" width="135" height="3" rx="1.5" fill="url(#c4)" opacity="0.3"/>
  <text x="652" y="100" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.35)" text-anchor="middle">129 / 740 sent to premium models</text>
</svg>

</div>

The system routes simple queries (Q&A, extraction, translation) to cheap models like Haiku/Mini/Llama 8B at near-zero cost, moderate tasks (summarization, analysis) to mid-tier models, and only escalates complex prompts (coding, math, planning) to premium models like Opus.

<div align="center">

<!-- Cost comparison bar chart SVG -->
<svg width="600" height="200" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barRouted" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff"/><stop offset="100%" stop-color="#3a7bd5"/>
    </linearGradient>
    <linearGradient id="barBaseline" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f093fb"/><stop offset="100%" stop-color="#f5576c"/>
    </linearGradient>
  </defs>
  <!-- Axis labels -->
  <text x="20" y="52" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.7)" text-anchor="start" font-weight="bold">Routed</text>
  <text x="20" y="112" font-family="Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.7)" text-anchor="start" font-weight="bold">Baseline</text>
  <!-- Routed bar -->
  <rect x="120" y="32" width="56" height="24" rx="4" fill="url(#barRouted)">
    <animate attributeName="width" from="0" to="56" dur="1.2s" fill="freeze"/>
  </rect>
  <text x="180" y="49" font-family="Arial,sans-serif" font-size="12" fill="url(#barRouted)" text-anchor="start">$0.020</text>
  <!-- Baseline bar -->
  <rect x="120" y="92" width="410" height="24" rx="4" fill="url(#barBaseline)">
    <animate attributeName="width" from="0" to="410" dur="1.2s" fill="freeze"/>
  </rect>
  <text x="534" y="109" font-family="Arial,sans-serif" font-size="12" fill="url(#barBaseline)" text-anchor="start">$0.264</text>
  <!-- Savings bracket -->
  <line x1="120" y1="62" x2="120" y2="88" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
  <line x1="56" y1="62" x2="56" y2="88" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
  <line x1="56" y1="62" x2="120" y2="62" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="88" y="80" font-family="Arial,sans-serif" font-size="11" fill="#43e97b" text-anchor="middle" font-weight="bold">92% saved</text>
  <!-- Percentage labels faded -->
  <text x="580" y="145" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.2)" text-anchor="end">Cost per 740 prompts</text>
</svg>

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

<!-- Feature cards with custom SVG icons -->
<div align="center">

| | | |
|---|---|---|
| <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="url(#cyanGrad)" stroke-width="1"/><text x="28" y="36" font-family="monospace" font-size="26" fill="#00d2ff" font-weight="bold" text-anchor="middle">9</text></svg><br/>**9 Models**<br/>GPT-4o, o1-mini, Claude<br/>Sonnet, Haiku, Opus, Llama | <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="url(#pinkGrad)" stroke-width="1"/><text x="28" y="36" font-family="monospace" font-size="22" fill="#f093fb" font-weight="bold" text-anchor="middle">ML</text></svg><br/>**ML Classifier**<br/>RandomForest + TF-IDF<br/>75%+ cross-val accuracy | <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="url(#greenGrad)" stroke-width="1"/><text x="28" y="36" font-family="monospace" font-size="24" fill="#43e97b" font-weight="bold" text-anchor="middle">₹</text></svg><br/>**Cost Optimizer**<br/>Route to cheapest model<br/>that meets quality needs |
| <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="url(#goldGrad)" stroke-width="1"/><text x="28" y="36" font-family="monospace" font-size="24" fill="#f6d365" font-weight="bold" text-anchor="middle">⚡</text></svg><br/>**Async by Default**<br/>True async concurrency<br/>across all providers | <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="#fff" stroke-width="1" stroke-opacity="0.15"/><text x="28" y="36" font-family="monospace" font-size="20" fill="rgba(255,255,255,0.7)" font-weight="bold" text-anchor="middle">DB</text></svg><br/>**DuckDB Logger**<br/>Request-level logs<br/>with cost & quality | <svg width="56" height="56" viewBox="0 0 56 56"><rect width="56" height="56" rx="14" fill="#1a1a2e"/><rect x="4" y="4" width="48" height="48" rx="12" fill="none" stroke="url(#cyanGrad)" stroke-width="1"/><text x="28" y="36" font-family="monospace" font-size="18" fill="#00d2ff" font-weight="bold" text-anchor="middle">API</text></svg><br/>**FastAPI + Docker**<br/>Production-ready API<br/>with Grafana dashboards |

</div>

---

## 🏗️ Architecture

<div align="center">

<!-- Architecture SVG diagram -->
<svg width="720" height="420" viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="boxBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a1a2e"/><stop offset="100%" stop-color="#16213e"/>
    </linearGradient>
    <linearGradient id="arrowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00d2ff"/><stop offset="100%" stop-color="#3a7bd5"/>
    </linearGradient>
    <filter id="shadow"><feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="rgba(0,0,0,0.4)"/></filter>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#3a7bd5"/>
    </marker>
  </defs>
  <!-- Background -->
  <rect width="720" height="420" rx="20" fill="#0f0c29" opacity="0.3"/>
  <!-- User Prompt -->
  <rect x="260" y="20" width="200" height="44" rx="10" fill="url(#boxBg)" stroke="url(#cyanGrad)" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="360" y="47" font-family="Arial,sans-serif" font-size="13" fill="#00d2ff" text-anchor="middle" font-weight="bold">User Prompt</text>
  <!-- Arrow down -->
  <line x1="360" y1="64" x2="360" y2="98" stroke="url(#arrowGrad)" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <!-- Classifier box -->
  <rect x="160" y="100" width="400" height="80" rx="12" fill="url(#boxBg)" stroke="url(#pinkGrad)" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="360" y="124" font-family="Arial,sans-serif" font-size="13" fill="#f093fb" text-anchor="middle" font-weight="bold">Complexity Classifier</text>
  <text x="230" y="148" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">TF-IDF</text>
  <text x="310" y="148" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">→</text>
  <text x="370" y="148" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">RandomForest</text>
  <text x="450" y="148" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">→</text>
  <text x="500" y="148" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">Ridge</text>
  <text x="360" y="168" font-family="Arial,sans-serif" font-size="9" fill="rgba(255,255,255,0.3)" text-anchor="middle">Tier + Score</text>
  <!-- Arrow down -->
  <line x1="360" y1="180" x2="360" y2="212" stroke="url(#arrowGrad)" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <!-- Router box -->
  <rect x="130" y="215" width="460" height="70" rx="12" fill="url(#boxBg)" stroke="url(#greenGrad)" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="360" y="239" font-family="Arial,sans-serif" font-size="13" fill="#43e97b" text-anchor="middle" font-weight="bold">Model Router</text>
  <!-- Tier pills -->
  <rect x="150" y="250" width="120" height="24" rx="12" fill="rgba(0,210,255,0.12)"/>
  <text x="210" y="266" font-family="Arial,sans-serif" font-size="10" fill="#00d2ff" text-anchor="middle" font-weight="bold">Tier 1 · Simple</text>
  <rect x="300" y="250" width="120" height="24" rx="12" fill="rgba(240,147,251,0.12)"/>
  <text x="360" y="266" font-family="Arial,sans-serif" font-size="10" fill="#f093fb" text-anchor="middle" font-weight="bold">Tier 2 · Moderate</text>
  <rect x="450" y="250" width="120" height="24" rx="12" fill="rgba(240,147,251,0.12)"/>
  <text x="510" y="266" font-family="Arial,sans-serif" font-size="10" fill="#f5576c" text-anchor="middle" font-weight="bold">Tier 3 · Complex</text>
  <!-- Arrow down -->
  <line x1="360" y1="285" x2="360" y2="318" stroke="url(#arrowGrad)" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <!-- LLM Provider strip -->
  <rect x="70" y="320" width="580" height="55" rx="12" fill="url(#boxBg)" stroke="rgba(255,255,255,0.1)" stroke-width="1" filter="url(#shadow)"/>
  <text x="360" y="340" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.4)" text-anchor="middle">LLM Providers</text>
  <rect x="100" y="346" width="140" height="22" rx="6" fill="#3a7bd5" opacity="0.2"/>
  <text x="170" y="361" font-family="Arial,sans-serif" font-size="10" fill="#00d2ff" text-anchor="middle">OpenAI (GPT-4o, Mini, o1)</text>
  <rect x="270" y="346" width="170" height="22" rx="6" fill="#f5576c" opacity="0.2"/>
  <text x="355" y="361" font-family="Arial,sans-serif" font-size="10" fill="#f093fb" text-anchor="middle">Anthropic (Sonnet, Haiku, Opus)</text>
  <rect x="470" y="346" width="150" height="22" rx="6" fill="#4facfe" opacity="0.2"/>
  <text x="545" y="361" font-family="Arial,sans-serif" font-size="10" fill="#4facfe" text-anchor="middle">Ollama (Llama 8B, 70B)</text>
  <!-- Arrow down -->
  <line x1="360" y1="375" x2="360" y2="395" stroke="url(#arrowGrad)" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <!-- Response -->
  <rect x="260" y="380" width="200" height="30" rx="10" fill="#43e97b" opacity="0.15" stroke="#43e97b" stroke-width="1" filter="url(#shadow)"/>
  <text x="360" y="399" font-family="Arial,sans-serif" font-size="12" fill="#43e97b" text-anchor="middle" font-weight="bold">Selected LLM Response</text>
</svg>

</div>

---

## 📊 Pricing Snapshot

<div align="center">

| Model | Provider | Input $/1M | Output $/1M | Latency | Quality | Best For |
|-------|----------|:----------:|:-----------:|:-------:|:-------:|----------|
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

# 6. Launch the API server
uvicorn app.main:app --reload

# 7. Run the 740-prompt benchmark
python run_benchmark.py

# 8. Run tests
python -m pytest tests/ -v
```

---

## 📁 Project Structure

```
LLM-Cost-AutoPilot/
├── app/                         # FastAPI service layer
│   ├── main.py                  # 4 endpoints: POST /v1/completions, GET /v1/stats, PUT /v1/routing-config, GET /health
│   ├── schemas.py               # Pydantic request/response models
│   ├── router_service.py        # RoutingService: classify → route → log → respond
│   └── config_store.py          # Runtime config via JSON file
├── core/                        # Core business logic
│   ├── router.py                # LLMRouter with tier→model fallback chain
│   ├── models_config.py         # 9 ModelConfig instances with real 2026 pricing
│   └── unified_interface.py     # Async LLM client (OpenAI + Anthropic + Ollama)
├── ml/                          # ML pipeline
│   ├── complexity_classifier.py # RandomForest + Ridge + TF-IDF classifier
│   ├── train_classifier.py      # Entry point: train, evaluate, save, generate routing map
│   └── __init__.py
├── storage/                     # Data persistence
│   └── duckdb_logger.py         # DuckDB schema, log, query, summary, baseline calc
├── verifier/                    # Quality verification pipeline
│   ├── async_verifier.py        # Async verifier with Langfuse + DuckDB
│   ├── classifier_feedback.py   # CSV feedback for classifier retraining loop
│   ├── judge_prompts.py         # LLM-as-judge agreement prompt template
│   ├── langfuse_logger.py       # Langfuse observability wrapper
│   └── reroute_handler.py       # Escalation to higher-tier models on failure
├── tests/                       # All test suites
│   ├── test_cost_tracker.py     # 16 tests — DuckDB logging + Grafan queries
│   ├── test_classifier.py       # 9 tests — training, prediction, routing map
│   ├── test_verifier.py         # 17 tests — pipeline, judge, feedback, reroute
│   ├── test_unified_interface.py # 22 tests — lazy init, routing, error handling
│   ├── test_models_config.py    # 32 tests — models, registry, cheapest selection
│   └── __init__.py
├── config/
│   ├── settings.py              # Env-driven configuration
│   └── routing_map.yaml         # Auto-generated tier→model mappings
├── data/
│   ├── complexity_labels.csv    # 234 labeled prompts across 14 task types
│   ├── llm_autopilot.duckdb     # Request-level DuckDB logs (gitignored)
│   └── report.txt               # Portfolio report
├── models/
│   └── complexity_classifier/   # Saved model artifacts (gitignored)
├── specs/                       # Implementation plans
├── Dockerfile                   # Python 3.11 slim container
├── docker-compose.yml           # API + Grafana + Ollama stack
├── run_benchmark.py             # 740-prompt portfolio benchmark
└── requirements.txt
```

---

## ✅ Test Suite

<div align="center">

| File | Tests | Status |
|------|:-----:|:------:|
| `tests/test_models_config.py` | 32 | ✅ Passing |
| `tests/test_unified_interface.py` | 22 | ✅ Passing |
| `tests/test_cost_tracker.py` | 16 | ✅ Passing |
| `tests/test_verifier.py` | 17 | ✅ Passing |
| `tests/test_classifier.py` | 9 | ✅ Passing |
| **Total** | **96** | **✅ All Passing** |

```bash
# Run all tests
python -m pytest tests/ -v
```

</div>

---

## 🛠️ Tech Stack

<div align="center">

| | |
|---|---|
| **Language** | Python 3.11+ |
| **API Framework** | FastAPI + Pydantic v2 |
| **ML Framework** | scikit-learn (RandomForest, Ridge, TF-IDF) |
| **LLM Providers** | OpenAI API · Anthropic API · Ollama (local) |
| **Storage** | DuckDB (embedded analytics) |
| **Observability** | Langfuse (LLM tracing) |
| **Data** | pandas, numpy, joblib, PyYAML |
| **Infrastructure** | Docker, Docker Compose, Grafana |
| **Testing** | pytest (96 tests) |

</div>

---

## 📈 Roadmap

- [x] **Day 1:** Unified model config + async interface + benchmark harness
- [x] **Day 2:** Complexity classifier (RandomForest + Ridge) + routing YAML
- [x] **Day 3:** Quality verifier pipeline — LLM-as-judge, Langfuse tracing, escalation
- [x] **Day 4:** DuckDB cost tracker — request logging, baseline comparison, Grafana queries
- [x] **Day 5:** FastAPI production API — POST /v1/completions, GET /v1/stats, PUT /v1/routing-config
- [x] **Portfolio:** 740-prompt benchmark, 92.3% cost reduction, 85.4% quality parity

---

<div align="center">

**LLM Cost Autopilot** · Built with ❤️

[![GitHub stars](https://img.shields.io/github/stars/shivamsingh-007/LLM-Cost-AutoPilot?style=social)](https://github.com/shivamsingh-007/LLM-Cost-AutoPilot)
[![GitHub forks](https://img.shields.io/github/forks/shivamsingh-007/LLM-Cost-AutoPilot?style=social)](https://github.com/shivamsingh-007/LLM-Cost-AutoPilot)

</div>
