import os
from pathlib import Path

os.environ["CYBER_DB_PATH"] = "data/test_cybersecurity.db"

from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_end_to_end_analysis_and_persistence():
    payload = {
        "event_id": "E-INTEGRATION-1",
        "timestamp": "2026-10-06T12:00:00Z",
        "source": "vpn-gateway",
        "event_type": "login_failure",
        "failed_attempts": 8,
        "known_bad_ip": 1,
        "privileged_account": 1,
        "severity": 0.9,
        "business_impact": 0.8,
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["predicted_label"] in {"benign", "suspicious"}
    assert 0 <= result["confidence"] <= 1
    assert 0 <= result["risk_score"] <= 100
    assert result["priority"] in {"low", "medium", "high"}

    history = client.get("/events").json()["events"]
    assert any(item["event_id"] == "E-INTEGRATION-1" for item in history)


def test_dashboard_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-Assisted Cybersecurity Risk Dashboard" in response.text
