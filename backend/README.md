# 🛡️ ScamShield OSS - Python Backend Engine

A high-speed, privacy-first scam intelligence backend built with **FastAPI**, **Pydantic V2**, and an **asymmetric hybrid heuristic engine**.

---

## ⚡ Core Architecture

ScamShield implements a two-stage evaluation pipeline:
1. **Deterministic Heuristic Rule Engine (0ms)**:
   - Evaluates messages and URLs across 6 categories (`urgency`, `financial`, `impersonation`, `credentials`, `technical`, `bait`).
   - Structural URL inspection (hyphen abuse, suspicious TLDs, disposable subdomains, brand typosquatting, raw IP targets).
   - Multi-category threat synergy calculations with calibrated probabilistic scoring.
2. **Local AI Threat Synthesizer**:
   - Queries **Local Ollama** (`http://localhost:11434`) using `gemma4:e2b` or other open models.
   - Generates an executive breakdown, psychological manipulation trigger, and 3 actionable defensive steps.
   - **Deterministic Fallback Engine**: If Ollama is offline or busy, immediately falls back to a 0ms deterministic rule explanation with 100% privacy and zero latency.

---

## 🚀 Quickstart

### 1. Activate Virtual Environment
```bash
cd backend
source venv/bin/activate
```

### 2. Install / Upgrade Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` (already configured with local defaults):
```bash
cp .env.example .env
```

### 4. Start the Backend Server
```bash
python run.py
```
Or directly with Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **API Base URL**: `http://localhost:8000`
- **Interactive OpenAPI Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Verification Tests

ScamShield Python backend includes a test suite verifying exact calibration matching the original benchmark targets:

```bash
# Run calibrated CLI benchmark test suite (colorful output)
python tests/test_scam_engine.py

# Run all unit and API integration tests via pytest
pytest tests
```

---

## 📡 API Reference

### 1. `GET /api/v1/health`
Checks backend status and detects local Ollama models.

**Response:**
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
  },
  "timestamp": "2026-10-26T06:06:42.123456+00:00"
}
```

---

### 2. `POST /api/v1/analyze`
Full analysis pipeline (Deterministic rules + Local AI synthesis).

**Request:**
```json
{
  "text": "Congratulations! You've won ₹50,000. Click now.",
  "type": "message",
  "model": "gemma4:e2b",
  "skipAiSynthesis": false
}
```

**Response:**
```json
{
  "riskScore": 75,
  "riskLevel": "HIGH_RISK",
  "riskLabel": "High Scam Risk",
  "summary": "This content scored a 75% risk rating due to detected threat patterns...",
  "indicators": [
    {
      "ruleId": "urgency_tactic",
      "title": "Urgency Pressure Tactic",
      "description": "Pressures recipient with immediate countdowns, deadlines, or rapid compliance language.",
      "category": "urgency",
      "severity": "high",
      "impactPercent": 34
    },
    {
      "ruleId": "cta_bait",
      "title": "Coerced Call-To-Action (Click Lure)",
      "description": "Aggressive instructions urging victim to click links or tap unverified portals.",
      "category": "urgency",
      "severity": "high",
      "impactPercent": 30
    },
    {
      "ruleId": "prize_bait",
      "title": "Prize & Lottery Bait",
      "description": "Lures victim with unexpected cash prizes, lotteries, lucky draws, or giveaways.",
      "category": "bait",
      "severity": "critical",
      "impactPercent": 40
    }
  ],
  "categoryScores": {
    "urgency": 64,
    "financial": 0,
    "impersonation": 0,
    "credentials": 0,
    "technical": 0,
    "bait": 40
  },
  "explanation": {
    "summary": "This message uses prize bait combined with urgency cues to lure clicks.",
    "psychologicalTrigger": "Greed & Curiosity Bait: Exploiting excitement around unearned prizes.",
    "actionItems": [
      "DO NOT click any links, scan QR codes, or download attachments provided.",
      "DO NOT disclose OTP, bank details, passwords, or personal identity numbers.",
      "Block the sender immediately and report the incident to cybercrime authorities."
    ],
    "source": "ollama_local"
  },
  "analyzedAt": "2026-10-26T06:06:42.123456+00:00",
  "type": "message"
}
```

---

### 3. `POST /api/v1/explain` (or `POST /api/explain`)
Drop-in replacement for the Next.js `/api/explain` route.

**Request:**
```json
{
  "text": "Dear SBI User, your account will be suspended within 24 hours due to pending KYC.",
  "riskScore": 96,
  "riskLevel": "CRITICAL_THREAT",
  "indicators": [],
  "model": "gemma4:e2b"
}
```

---

## 🔗 Connecting Frontend to Python Backend

You can connect the Next.js frontend to the Python backend in two ways:

### Option A: Next.js API Rewrite (Recommended)
Add a rewrite in `next.config.ts`:
```ts
const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/py/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/:path*',
      },
      {
        source: '/api/explain',
        destination: 'http://127.0.0.1:8000/api/explain',
      },
    ];
  },
};
```

### Option B: Direct Fetch from Client
With FastAPI CORS configured for `http://localhost:3000`, the frontend can directly call:
```ts
const res = await fetch('http://localhost:8000/api/v1/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text, type }),
});
```
