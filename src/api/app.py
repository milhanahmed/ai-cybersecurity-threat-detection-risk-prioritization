"""Integrated FastAPI application for the capstone prototype."""

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.database.database import init_db, list_analyses, save_analysis
from src.ingestion.ingestion import validate_event
from src.models.classifier import ThreatClassifier
from src.preprocessing.preprocessing import normalize_event
from src.risk_scoring.risk_score import calculate_risk_score, priority_from_score

app = FastAPI(title="AI Cybersecurity Threat Detection and Risk Prioritization")

BASELINE_FEATURES = [
    {"event_type": "login_success", "failed_attempts": 0, "known_bad_ip": 0, "privileged_account": 0},
    {"event_type": "file_read", "failed_attempts": 0, "known_bad_ip": 0, "privileged_account": 0},
    {"event_type": "login_failure", "failed_attempts": 2, "known_bad_ip": 0, "privileged_account": 0},
    {"event_type": "login_failure", "failed_attempts": 8, "known_bad_ip": 1, "privileged_account": 1},
    {"event_type": "malware_alert", "failed_attempts": 0, "known_bad_ip": 1, "privileged_account": 0},
    {"event_type": "privilege_change", "failed_attempts": 1, "known_bad_ip": 0, "privileged_account": 1},
]
BASELINE_LABELS = ["benign", "benign", "benign", "suspicious", "suspicious", "suspicious"]

classifier = ThreatClassifier().fit(BASELINE_FEATURES, BASELINE_LABELS)
init_db()


class AnalyzeRequest(BaseModel):
    event_id: str
    timestamp: str
    source: str
    event_type: str
    failed_attempts: int = 0
    known_bad_ip: int = 0
    privileged_account: int = 0
    severity: float = 0.5
    business_impact: float = 0.5


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> Dict[str, Any]:
    raw = request.model_dump()
    event = {k: raw[k] for k in ("event_id", "timestamp", "source", "event_type")}
    if not validate_event(event):
        raise HTTPException(status_code=400, detail="Required event fields are missing.")

    event = normalize_event(event)
    features = {
        "event_type": event["event_type"],
        "failed_attempts": request.failed_attempts,
        "known_bad_ip": request.known_bad_ip,
        "privileged_account": request.privileged_account,
    }
    prediction = classifier.predict(features)
    score = calculate_risk_score(request.severity, prediction.confidence, request.business_impact)
    priority = priority_from_score(score)

    result = {
        **event,
        "predicted_label": prediction.label,
        "confidence": prediction.confidence,
        "risk_score": score,
        "priority": priority,
    }
    save_analysis(result)
    return result


@app.get("/events")
def events(limit: int = 50):
    return {"events": list_analyses(limit=max(1, min(limit, 100)))}


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    dashboard_path = Path(__file__).resolve().parents[1] / "dashboard" / "index.html"
    return dashboard_path.read_text(encoding="utf-8")
