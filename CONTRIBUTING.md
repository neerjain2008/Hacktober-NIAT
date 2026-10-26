# 🤝 Contributing to ScamShield OSS

Thank you for your interest in contributing to **ScamShield OSS**! We welcome developers, cybersecurity researchers, accessibility advocates, and students worldwide to help protect people from cyber fraud.

---

## 📜 Code of Conduct & Privacy Guarantee
All contributors must strictly respect ScamShield's core architectural principle:
* **Zero Database / Zero Log**: Never submit code that introduces persistent databases, user tracking cookies, telemetry pixels, or server-side logging of user messages.
* **Respectful Community**: Treat all contributors and users with kindness, empathy, and professional respect.

---

## 🛠️ Local Development Setup

### 1. Fork & Clone
```bash
git clone https://github.com/<your-username>/ScamShield-oss.git
cd ScamShield-oss
```

### 2. Frontend Development (Next.js 16)
```bash
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the live dashboard.

### 3. Backend Development (FastAPI Python)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore interactive OpenAPI Swagger docs.

---

## 🧪 Testing Guidelines

Before opening a pull request, you **must ensure all tests pass**:

```bash
# 1. Run Frontend Verification Suite
npm test

# 2. Run Backend Python Verification Suite
pytest backend/tests

# 3. Run Benchmark Parity Check
python backend/tests/test_scam_engine.py
```

---

## 💡 How to Add a New Scam Heuristic Rule

When contributing a new detection pattern, ensure it is added to **both** the TypeScript and Python engines:

1. **TypeScript Engine**: [`src/lib/scamEngine.ts`](src/lib/scamEngine.ts) in `MESSAGE_RULES` or `analyzeUrl`.
2. **Python Engine**: [`backend/app/core/rules.py`](backend/app/core/rules.py) or [`backend/app/core/url_analyzer.py`](backend/app/core/url_analyzer.py).
3. **Calibrate Weight**: Assign a realistic probability factor ($p_i \in [0.10, 0.45]$) based on severity.
4. **Add a Test Case**: Add an example string to `test-cli.mjs` and `backend/tests/test_scam_engine.py`.

---

## 📬 Pull Request Workflow

1. Create a feature branch: `git checkout -b feature/crypto-giveaway-detector`.
2. Commit with concise semantic commit messages:
   - `feat: add WhatsApp order grabbing heuristic`
   - `fix: correct regex boundary for UPI handle checks`
   - `docs: update deployment guidelines`
3. Push to your fork: `git push origin feature/crypto-giveaway-detector`.
4. Open a Pull Request against `main`. Ensure all CI checks pass.
