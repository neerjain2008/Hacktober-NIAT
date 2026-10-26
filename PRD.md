# 📋 ScamShield OSS — Product Requirements Document (PRD)

**Document Version:** 2.0.0  
**Status:** Approved & Implemented  
**Author:** ScamShield Core Team  
**Classification:** Open Source Public Specification  

---

## 1. Executive Summary & Product Vision

### 1.1 Vision Statement
To democratize enterprise-grade cyber fraud intelligence by delivering a **zero-log, privacy-guaranteed, open-source scam detection engine** that protects vulnerable populations from digital deception without harvesting personal correspondence.

### 1.2 Core Philosophy: Privacy-First Asymmetric Defense
Traditional security tools compromise victim privacy by uploading emails, SMS messages, and screenshots to remote clouds. ScamShield OSS is founded on three unbreakable tenets:
1. **Zero Data Retention**: No databases, no user accounts, no telemetry, no tracking cookies.
2. **Deterministic Rules First**: Mathematical heuristics execute in 0 milliseconds in local memory (RAM) with 100% predictable scoring.
3. **100% On-Device AI**: Contextual threat explanations and psychological manipulation analyses run locally via open-weights models (Ollama `gemma4:e2b` / `llama3.2`) or instant deterministic fallback templates.

---

## 2. Problem Statement & Market Need

### 2.1 The Cyber Fraud Epidemic
Digital financial fraud, smishing (SMS phishing), task-based work-from-home scams, and bank impersonation schemes cause over **$1 trillion in annual losses globally**. The primary victims are elderly citizens, students, and non-technical individuals who struggle to identify subtle psychological manipulation tactics (urgency pressure, authority mimicry, prize euphoria).

### 2.2 The Privacy Dilemma of Existing Solutions
Current scam checkers suffer from critical architectural flaws:
* **Surveillance & Data Leaks**: Uploading private chat screenshots or SMS notifications to cloud services exposes confidential OTPs, bank balances, and family conversations.
* **LLM Hallucinations**: Generic AI wrappers frequently assign arbitrary, non-reproducible risk scores to benign messages or miss zero-day phishing heuristics.
* **Accessibility Blindness**: Most cybersecurity software fails WCAG accessibility standards, alienating seniors and visually impaired users who are statistically the most vulnerable.

---

## 3. Target User Personas

### Persona 1: The Vulnerable Senior Citizen
* **Name**: Ramesh, Age 68 (Retired Government Officer)
* **Context**: Frequently receives urgent SMS warnings claiming his electricity bill is overdue or his SBI netbanking KYC will be blocked within 24 hours.
* **Needs**: Large, legible fonts (high contrast), simple plain-language guidance, and an audio narrator that reads aloud whether the message is a scam.
* **Value Delivered**: Text Magnifier (145% zoom), High Contrast AAA Dark/Light modes, and one-click Web Speech Audio Readout.

### Persona 2: The Freelancer / Job Seeker
* **Name**: Ananya, Age 23 (College Graduate & Freelancer)
* **Context**: Actively seeking remote work; receives unsolicited Telegram and WhatsApp invitations offering ₹5,000/day for liking YouTube videos or rating hotels.
* **Needs**: Instant verification of job validity before paying "security registration fees" or sharing bank account numbers.
* **Value Delivered**: 0ms detection of advance-fee job scams, off-platform redirection alerts, and actionable next steps.

### Persona 3: The Cybersecurity Analyst / First Responder
* **Name**: Marcus, Age 34 (SOC Analyst / Incident Responder)
* **Context**: Investigates suspicious phishing links and disposable infrastructure for friends, family, and enterprise users.
* **Needs**: Transparent, explainable indicators showing exact regex matches, domain age anomalies, punycode spoofing, and API integration.
* **Value Delivered**: Python FastAPI backend with OpenAPI Swagger docs (`/docs`), explainable indicator breakdowns, and 100% offline self-hosting.

---

## 4. User Stories & Acceptance Criteria

| ID | User Story | Acceptance Criteria |
| :--- | :--- | :--- |
| **US-01** | As a user, I want to paste a suspicious SMS or WhatsApp message so that I know its danger level immediately. | • Engine returns a score (0–100%) and clear risk tier within 50ms.<br/>• Triggered indicators display with impact percentages.<br/>• No text is saved to any database. |
| **US-02** | As a user, I want to scan a URL without clicking it so that I don't trigger drive-by malware or credential theft. | • Evaluates domain for typosquatting, hyphen abuse, naked IPs, and abusive TLDs.<br/>• Official brand domains (e.g., `amazon.com`, `sbi.co.in`) are not falsely flagged. |
| **US-03** | As a user, I want to paste a screenshot directly from my clipboard (`Ctrl+V`) so that I don't have to manually type long messages. | • Optical Character Recognition (OCR) runs in-browser via Tesseract.js WebAssembly.<br/>• Image bytes never leave client RAM.<br/>• Recognized text feeds directly into analysis card. |
| **US-04** | As a visually impaired user, I want to hear the threat summary spoken aloud so that I can understand the danger without straining to read. | • Voice Readout button plays synthesized audio using Web Speech API.<br/>• Speaks risk score, danger level, psychological trap, and action items. |
| **US-05** | As an elderly user, I want high-contrast and enlarged text modes so that I can easily navigate the interface. | • 4-tier font scaler rescales root rem units dynamically.<br/>• High Contrast Dark mode enforces >= 7:1 contrast ratio with yellow/white text and pure black canvas. |
| **US-06** | As a developer, I want a Python REST API so that I can integrate ScamShield into mobile apps, email gateways, and bots. | • FastAPI backend exposes `/api/v1/analyze`, `/api/v1/explain`, and `/api/v1/health`.<br/>• OpenAPI Swagger docs available at `/docs`.<br/>• 100% test pass on benchmark cases. |

---

## 5. Functional Requirements

### 5.1 Multi-Scanner Ingestion (FR-1)
* **FR-1.1**: The system must provide three primary input tabs: Message, URL, and Screenshot.
* **FR-1.2**: Screenshot tab must support file upload, drag-and-drop, clipboard paste (`Ctrl+V`), and a 1-click synthetic sample generator.
* **FR-1.3**: Character counter with dynamic length limits and one-click clear button.

### 5.2 Deterministic Heuristic Engine (FR-2)
* **FR-2.1**: The engine must inspect input against 6 distinct threat vectors: Urgency, Call-to-Action Bait, Prize/Lottery Lures, Advance Payment Demands, Authority Impersonation, and Credential Harvesting.
* **FR-2.2**: The engine must evaluate URL tokens for hyphen spamming, numeric hosts, brand mimicry, and high-risk TLDs (`.xyz`, `.top`, `.tk`, etc.).
* **FR-2.3**: Mathematical score compounding must utilize asymptotic Bayesian survival probability: $P = 1 - \prod(1 - p_i)$.
* **FR-2.4**: Multi-category attack synergy factor must boost risk scores when $\ge 2$ distinct categories match simultaneously.

### 5.3 On-Device AI Threat Synthesizer (FR-3)
* **FR-3.1**: The system must asynchronously query a local Ollama daemon on `localhost:11434` for contextual threat summaries.
* **FR-3.2**: Output must be validated against a strict JSON schema containing: `summary` (2 sentences), `psychologicalTrigger`, and `actionItems` (exactly 3 items).
* **FR-3.3**: In the event of Ollama unavailability or timeout (>20s), the system must execute an immediate deterministic fallback explanation in 0ms.

### 5.4 WCAG AAA Vision & Accessibility Suite (FR-4)
* **FR-4.1**: 4-level root font scaling: 100% (16px), 118% (19px), 137% (22px), and 162% (26px).
* **FR-4.2**: WCAG AAA High Contrast Dark: `#000000` canvas, 2px solid white borders, high-visibility `#ffff00` typography.
* **FR-4.3**: WCAG AAA High Contrast Light: `#ffffff` canvas, pitch-black text, 2px borders.
* **FR-4.4**: Dyslexia mode: expanded letter-spacing (0.08em), word spacing (0.16em), and line-height (1.85).
* **FR-4.5**: Reduced motion toggle: disables CSS animations, scanline sweeps, and pulse effects.
* **FR-4.6**: Text-to-Speech (TTS) engine powered by browser `SpeechSynthesis` with play/stop toggle.

### 5.5 Python Service Gateway (FR-5)
* **FR-5.1**: FastAPI backend running on port 8000.
* **FR-5.2**: Pydantic V2 request/response schemas with automatic camelCase / snake_case serialization.
* **FR-5.3**: Local Ollama auto-discovery endpoint returning available models (`GET /api/v1/health`).
* **FR-5.4**: Parity verification test suite achieving 100% pass on benchmark scenarios.

---

## 6. Non-Functional Requirements (NFRs)

### 6.1 Privacy & Data Governance (NFR-1)
* **NFR-1.1**: The platform must maintain a strict **Zero-Database** architecture. No relational or document databases may be introduced.
* **NFR-1.2**: The platform must not set tracking cookies, local identifier tokens, or third-party analytics pixels.
* **NFR-1.3**: All scanned user data must reside exclusively in volatile RAM and be garbage collected upon request completion.

### 6.2 Latency & Performance SLAs (NFR-2)
* **NFR-2.1**: Deterministic heuristic evaluation latency must be **< 10ms** for messages up to 10,000 characters.
* **NFR-2.2**: In-browser Wasm OCR initialization and extraction must complete in **< 3.0s** on modern mobile and desktop browsers.
* **NFR-2.3**: AI threat synthesis must deliver responses within **< 5.0s** on hardware-accelerated local Ollama runners.

### 6.3 Accessibility & Universal Design (NFR-3)
* **NFR-3.1**: Contrast ratios in default mode must exceed **4.5:1** (WCAG AA). Contrast ratios in High Contrast modes must exceed **7:1** (WCAG AAA).
* **NFR-3.2**: All interactive controls must support full keyboard navigation (`Tab`, `Shift+Tab`, `Enter`, `Space`) with visible focus outlines (`3px solid #06b6d4` or `#ffff00`).

### 6.4 Reliability & Portability (NFR-4)
* **NFR-4.1**: The web application must build into a self-contained production Docker container (`node:22-alpine`) executable in air-gapped environments.
* **NFR-4.2**: The Python backend must run without external cloud dependencies, requiring only Python 3.9+ and pip dependencies.

---

## 7. Assumptions, Dependencies & Risks

### 7.1 Assumptions
* Users have access to modern evergreen browsers (Chrome 100+, Safari 16+, Firefox 100+, Edge) supporting WebAssembly and the Web Speech API.
* Users desiring AI-generated summaries have Ollama installed locally with at least 4GB of free RAM for running lightweight open models (`gemma4:e2b` or `llama3.2:3b`).

### 7.2 Dependencies
* **Frontend**: Next.js 16, React 19, Tailwind CSS v4, Framer Motion, Tesseract.js.
* **Backend**: FastAPI, Uvicorn, Pydantic V2, httpx, python-dotenv, pytest.
* **AI Service**: Local Ollama daemon running on `localhost:11434`.

### 7.3 Risk Mitigation Matrix
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Local Ollama is offline or uninstalled** | Medium | Built-in 0ms deterministic fallback engine synthesizes threat summaries automatically; user experience remains seamless. |
| **User pastes highly confidential OTP/credentials** | Critical | Zero-log guarantee ensures text is never saved to disk or transmitted to cloud servers; RAM is discarded immediately. |
| **Slow OCR performance on low-end mobile devices** | Low | Wasm worker runs in background thread to prevent UI freezing; clear loading spinner and status feedback provided. |

---

## 8. Success Metrics & Key Performance Indicators (KPIs)

1. **Privacy Invariance**: 0 data leakage incidents, 0 tracking requests, 0 bytes persisted to disk.
2. **Detection Accuracy**: $\ge 95\%$ accuracy on benchmark smishing, task fraud, and phishing URL datasets.
3. **Accessibility Compliance**: 100% compliance with WCAG 2.2 Level AAA standards in High Contrast modes.
4. **Adoption & Developer Community**: GitHub stars, forks, and contributions across hackathons (MLH, Hacktoberfest) and open-source cybersecurity collectives.
