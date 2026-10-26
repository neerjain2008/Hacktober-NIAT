import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "api_v1" in data


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ollama" in data


def test_analyze_endpoint_prize_bait():
    payload = {
        "text": "Congratulations! You've won ₹50,000. Click now.",
        "type": "message",
        "skip_ai_synthesis": True,
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "riskScore" in data or "risk_score" in data
    score = data.get("riskScore", data.get("risk_score"))
    assert 70 <= score <= 89
    assert data["riskLevel"] in ["HIGH_RISK", "CRITICAL_THREAT"]
    assert len(data["indicators"]) >= 2
    assert "explanation" in data


def test_explain_endpoint_fallback():
    payload = {
        "text": "Dear SBI User, your account will be suspended within 24 hours due to pending KYC.",
        "riskScore": 96,
        "riskLevel": "CRITICAL_THREAT",
        "indicators": [
            {
                "ruleId": "urgency_tactic",
                "title": "Urgency Pressure Tactic",
                "description": "Pressures recipient with immediate countdowns.",
                "category": "urgency",
                "severity": "high",
                "impactPercent": 34,
            }
        ],
        "model": "gemma4:e2b",
    }
    response = client.post("/api/v1/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "explanation" in data
    assert len(data["explanation"]["actionItems"]) == 3
