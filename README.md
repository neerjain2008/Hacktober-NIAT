# 🛡️ ScamShield OSS
### High-Speed, Privacy-Guaranteed Cyber Fraud Intelligence Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Frontend: Next.js 16](https://img.shields.io/badge/Frontend-Next.js%2016%20%2F%20React%2019-black.svg)](ARCHITECTURE.md#1-frontend-presentation-tier)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%2F%20Python%203.9%2B-009688.svg)](ARCHITECTURE.md#2-backend-service-tier-fastapi)
[![Inference: Local Ollama](https://img.shields.io/badge/AI-100%25%20On--Device%20Ollama-FF6F00.svg)](ARCHITECTURE.md#4-aiml-inference-tier)
[![Accessibility: WCAG 2.2 AAA](https://img.shields.io/badge/Accessibility-WCAG%202.2%20AAA-brightgreen.svg)](DESIGN.md#6-accessibility-design--wcag-22-aaa-suite)
[![Privacy: Zero-Database](https://img.shields.io/badge/Privacy-Zero--Database%20RAM%20Only-emerald.svg)](PRIVACY.md)
[![Tests: 100% Calibrated](https://img.shields.io/badge/Tests-100%25%20Passing-success.svg)](#-verification-test-suite)

> **ScamShield OSS** is an open-source, privacy-first cybersecurity engine engineered to detect smishing, phishing URLs, advance-fee frauds, and chat scams in real time. Built with a **0ms deterministic heuristic engine**, **in-browser WebAssembly OCR**, a **decoupled FastAPI Python service**, and **100% on-device local AI via Ollama** with zero cloud transmission.

---

## ⚡ 1-Click Cloud & Container Deploy

Deploy ScamShield OSS instantly to **DigitalOcean App Platform** or run locally via Docker:

[![Deploy to DigitalOcean](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new)

```bash
# Run the hermetic, air-gapped production Docker container:
docker build -t scamshield-oss .
docker run -p 3000:3000 scamshield-oss
```

---

## 🚨 Problem Statement vs. ScamShield Solution

| Traditional Scam Checkers | The ScamShield OSS Architecture |
| :--- | :--- |
| ❌ **Cloud Surveillance**: Uploads your private chats, SMS, and OTPs to remote vendor servers. | 🔒 **Strict Zero-Log Guarantee**: No databases, no user accounts, no tracking cookies. Data exists purely in ephemeral RAM and vanishes on tab close. |
| ❌ **Hallucinating Cloud AI**: Prompts generic cloud LLMs that invent arbitrary, non-reproducible risk percentages. | ⚡ **Deterministic Heuristics First**: Mathematical risk math executes in 0ms via Bayesian probability compounding with 100% predictable scoring. |
| ❌ **High Latency & Cloud Costs**: Every scan costs API credits and requires multi-second round trips. | 💰 **Zero Cost & Offline-Ready**: 100% on-device local inference via Ollama (`gemma4:e2b`, `llama3.2`) with 0ms deterministic natural-language fallback. |
| ❌ **Accessibility Blindness**: Cluttered interfaces that alienate elderly and visually impaired users. | ♿ **WCAG 2.2 Level AAA Certified**: 4-level root font scaling, pure high-contrast AAA modes, dyslexia readability, and voice audio narration. |

---

## 🎯 The Core Innovation: Asymmetric Hybrid Engine

Rather than relying on naive LLM wrappers, ScamShield separates **quantitative threat scoring** from **qualitative natural-language explanation**:

```
[ Input: SMS / WhatsApp / URL / Screenshot ]
                     │
                     ▼
       ┌───────────────────────────┐
       │ In-Browser WebAssembly    │  <-- Tesseract.js Wasm (Screenshots never leave device)
       │ OCR Text Extraction       │
       └───────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │ Deterministic Heuristic   │  <-- 0ms, 130+ Regex Patterns, URL Typosquatting Analyzer
       │ Rule Engine (TS / Python) │
       └───────────────────────────┘
                     │
                     ├─ Mathematical Risk Score (e.g. 87%)
                     ├─ Severity Tier Classification (Safe -> Critical Threat)
                     ├─ Multi-Category Attack Synergy Factor (+3% to +9%)
                     └─ Triggered Heuristic Indicators (Impact Badges)
                     │
                     ▼
       ┌───────────────────────────┐
       │ Local AI Threat           │  <-- Local Ollama (gemma4:e2b / llama3.2 on localhost:11434)
       │ Synthesizer (Ollama API)  │      *With 0ms Deterministic Natural-Language Fallback*
       └───────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │ Security Dashboard Result │  <-- Animated Radar Gauge + Cognitive Manipulation Trap
       │ & Voice Threat Readout    │      + 3 Immediate Defensive Action Items + TTS Audio
       └───────────────────────────┘
```

---

## 🔍 The 3 Scanners (1 Shared Intelligence Engine)

| Scanner | Input Ingestion | Key Detection Capabilities |
| :--- | :--- | :--- |
| **💬 Message Scanner** | SMS, WhatsApp, Telegram, Email strings | Scans for urgency traps (`within 24 hours`), advance fee demands (`registration fee`), lottery lures (`₹50,000 cash prize`), bank KYC impersonation (`SBI`, `HDFC`, `Netflix`), and credential/OTP theft. |
| **🔗 URL Scanner** | Raw URL or domain name | Evaluates hyphen abuse (`amazon-prize-2026.net`), numeric subdomain stuffing, brand typosquatting, abusive disposable TLDs (`.xyz`, `.top`, `.tk`), naked IP hosts, and nested redirection. |
| **📸 Screenshot Scanner** | Chat screenshots, image upload, clipboard paste (`Ctrl+V`) | Executes **Tesseract.js WebAssembly OCR** entirely within the browser sandbox. **Images never leave client RAM.** Automatically routes extracted text into the heuristic engine. Includes an instant **1-Click Synthetic Sample Generator**. |

---

## ♿ Accessibility & Vision Suite (WCAG 2.2 AAA Certified)

ScamShield OSS is designed specifically for seniors and visually impaired individuals who are disproportionately targeted by cybercriminals:

1. **Dynamic Text Magnifier**: 4-level root font scaling (`100%`, `118% A+`, `137% A++`, `162% Max Zoom`) dynamically resizing every card, button, and indicator.
2. **High Contrast Dark (AAA)**: Pitch-black (`#000000`) canvas with 2px solid white borders and high-visibility `#FFFF00` (yellow) typography exceeding **7:1 contrast ratios**.
3. **High Contrast Light (AAA)**: Pure white (`#FFFFFF`) background with stark black (`#000000`) text and solid structural borders.
4. **Voice Threat Readout (TTS)**: Built-in Web Speech API audio narrator that vocalizes the risk score, detected trap, and recommended protective actions.
5. **Dyslexia Reading Mode**: Expanded letter-spacing (`0.08em`), word-spacing (`0.16em`), and line-heights (`1.85`).
6. **Vestibular Safety (Reduced Motion)**: Completely eliminates radar scanline animations and gauge pulses for vestibular safety.

---

## 🛠️ Technology Stack

```
ScamShield OSS
├── Presentation Layer (Frontend)
│   ├── Next.js 16 (App Router) & React 19
│   ├── Tailwind CSS v4 & Vanilla CSS Variables
│   ├── Framer Motion (Transitions, Scanline Sweeps, Radar Pulses)
│   ├── Tesseract.js (In-Browser WebAssembly Optical Character Recognition)
│   └── Web Speech API (Native SpeechSynthesis Voice Threat Readout)
├── Service Tier (Python Backend)
│   ├── FastAPI & Uvicorn (High-performance async ASGI server)
│   ├── Pydantic V2 (Strict schema validation with camelCase / snake_case parity)
│   ├── HTTPX (Non-blocking async HTTP networking)
│   └── Pytest (Automated unit & API integration testing)
├── Inference Tier (AI / Heuristics)
│   ├── Deterministic Heuristic Rule Registry (TypeScript & Python dual engines)
│   ├── Local Ollama Daemon (localhost:11434 with gemma4:e2b / llama3.2)
│   └── Zero-Latency Deterministic Explanation Fallback Engine
└── Infrastructure & Tooling
    ├── Docker (Multi-stage node:22-alpine container)
    └── DigitalOcean App Platform (.do/app.yaml deployment spec)
```

---

## 🚀 Quickstart Guide

### Prerequisites
* **Node.js**: v18+ (tested on Node.js 22) and npm 9+
* **Python**: v3.9+ (optional, for running the FastAPI service)
* **Local Ollama** *(optional, for local AI threat synthesis)*: [ollama.com](https://ollama.com)

---

### Step 1: Clone Repository
```bash
git clone https://github.com/neerjain2008/ScamShield-oss.git
cd ScamShield-oss
```

---

### Step 2: Start the Next.js Frontend
```bash
# Install frontend dependencies
npm install

# Start development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

### Step 3: Start the Python Backend (Optional / Standalone API)
```bash
cd backend

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install -r requirements.txt

# Run FastAPI development server
python run.py
```
* **Interactive OpenAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Service Health & Ollama Status**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### Step 4: Local Ollama Setup (100% On-Device AI)
ScamShield connects to local Ollama on `http://localhost:11434`. Pull any open-weight model:
```bash
# Pull the recommended lightweight model:
ollama pull gemma4:e2b

# Or an alternative open model:
ollama pull llama3.2:3b
```
*(If Ollama is not running, ScamShield seamlessly falls back to its built-in 0ms deterministic natural-language explanation engine with zero disruption).*

---

## 🧪 Verification Test Suite

ScamShield includes automated benchmark suites verifying heuristic scoring calibration against established test cases:

```bash
# 1. Run the Node.js verification CLI suite:
node test-cli.mjs

# 2. Run the Python benchmark CLI verification suite:
python backend/tests/test_scam_engine.py

# 3. Run all Python unit and API integration tests:
pytest backend/tests
```

### Benchmark Calibration Matrix:
| Test Scenario | Input Snippet | Target Range | Engine Score | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Prize Bait** | `"Congratulations! You've won ₹50,000. Click now."` | 70% – 89% | **75%** | ✅ PASSED |
| **Phishing URL** | `"amazon-prize-2026.net"` | 72% – 84% | **79%** | ✅ PASSED |
| **Urgent KYC SMS** | `"Dear SBI User, your account will be suspended within 24 hours..."` | 85% – 96% | **96%** | ✅ PASSED |
| **Task Fraud** | `"Earn ₹8,000 daily by liking YouTube videos. Deposit ₹1,500..."` | 80% – 92% | **87%** | ✅ PASSED |
| **Mild Urgency** | `"Please note this is urgent for our meeting tomorrow."` | 22% – 40% | **34%** | ✅ PASSED |
| **Clean Alert** | `"GitHub Security: A new personal access token was generated..."` | 2% – 10% | **5%** | ✅ PASSED |
| **Clean Personal**| `"Hey Neer, are we still meeting for lunch at 1pm tomorrow..."` | 4% – 12% | **7%** | ✅ PASSED |
| **Clean Corporate**| `"Dear Team, Please find attached the quarterly analytics report..."` | 3% – 10% | **6%** | ✅ PASSED |

---

## 📡 REST API Reference (FastAPI Backend)

### 1. Health & Model Discovery
```http
GET /api/v1/health
```
```json
{
  "status": "healthy",
  "service": "ScamShield OSS Backend",
  "version": "1.0.0",
  "ollama": {
    "ollama_online": true,
    "base_url": "http://localhost:11434",
    "models_available": ["gemma4:e2b"],
    "default_model": "gemma4:e2b"
  }
}
```

### 2. Unified Threat Analysis
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Congratulations! You've won ₹50,000. Click now.",
  "type": "message",
  "model": "gemma4:e2b",
  "skipAiSynthesis": false
}
```
```json
{
  "riskScore": 75,
  "riskLevel": "HIGH_RISK",
  "riskLabel": "High Scam Risk",
  "indicators": [
    {
      "ruleId": "prize_bait",
      "title": "Prize & Lottery Bait",
      "category": "bait",
      "severity": "critical",
      "impactPercent": 40
    }
  ],
  "explanation": {
    "summary": "This message uses prize bait combined with urgency cues to lure clicks.",
    "psychologicalTrigger": "Greed & Curiosity Bait: Exploiting excitement around unearned prizes.",
    "actionItems": [
      "DO NOT click any links, scan QR codes, or download attachments.",
      "DO NOT disclose OTP, bank details, passwords, or personal identity numbers.",
      "Block the sender immediately and report the incident to cybercrime authorities."
    ],
    "source": "ollama_local"
  }
}
```

---

## 🏆 Hackathon 1-Click Demo Scenarios

Judges and evaluators can instantly test ScamShield using the interactive preset bar in the UI:
- 🎁 **Amazon ₹50k Prize Bait** (`Score: 75% High Scam Risk`)
- 🚨 **Fake SBI Bank KYC SMS** (`Score: 96% Critical Threat`)
- 💼 **Telegram YouTube Like Scam** (`Score: 87% Critical Threat`)
- 🔗 **Phishing URL: netflix-login-verify.top** (`Score: 96% Critical Threat`)
- 🛡️ **Legitimate GitHub Security Alert** (`Score: 5% Safe / Low Threat`)

---

## 📖 Comprehensive Documentation Suite

For deep technical specifications, design tokens, and project governance, explore our complete documentation index:

* [**ARCHITECTURE.md**](ARCHITECTURE.md) — Complete system architecture, Mermaid data-flow diagrams, and mathematical formulas.
* [**PRD.md**](PRD.md) — Product Requirements Document detailing user personas, functional specifications, and SLAs.
* [**DESIGN.md**](DESIGN.md) — Design system, typography, Halftone LED canvas, color tokens, and WCAG AAA accessibility.
* [**ROADMAP.md**](ROADMAP.md) (or [**PHASES.md**](PHASES.md)) — 5-Phase strategic development timeline (Phases 1–5).
* [**PRIVACY.md**](PRIVACY.md) — Zero-Log architectural guarantees and data protection policies.
* [**backend/README.md**](backend/README.md) — Dedicated Python FastAPI backend documentation.

---

## 🤝 Contributing & Community Guidelines

ScamShield OSS is an open-source initiative built with ❤️ for **Hacktoberfest** and the **MLH Open-Source AI Challenge**. We welcome contributions from developers, cybersecurity researchers, and accessibility advocates worldwide!

1. **Fork the Repository**: Click `Fork` on GitHub.
2. **Create a Feature Branch**: `git checkout -b feature/new-threat-indicator`.
3. **Add Tests**: Ensure new regex patterns or features pass both `node test-cli.mjs` and `pytest backend/tests`.
4. **Commit Changes**: Use semantic commit messages (`feat: add crypto giveaway heuristic rule`).
5. **Open a Pull Request**: Submit your PR with a concise description of your improvements.

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.
