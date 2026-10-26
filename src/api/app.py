"""Integrated FastAPI application for the capstone prototype."""

from pathlib import Path
from datetime import datetime
from typing import Literal
import os
import secrets
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, ConfigDict
from fastapi.security import HTTPBasic, HTTPBasicCredentials

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


security = HTTPBasic(auto_error=False)


def require_analyst(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    expected_user = os.environ.get("CYBER_USERNAME", "")
    expected_password = os.environ.get("CYBER_PASSWORD", "")
    if not expected_user or len(expected_password) < 16:
        raise HTTPException(status_code=503, detail="Analyst credentials are not configured.")
    user = credentials.username.encode("utf-8") if credentials else b""
    password = credentials.password.encode("utf-8") if credentials else b""
    valid_user = secrets.compare_digest(user, expected_user.encode("utf-8"))
    valid_password = secrets.compare_digest(password, expected_password.encode("utf-8"))
    if not (valid_user and valid_password):
        raise HTTPException(status_code=401, detail="Authentication required.",
                            headers={"WWW-Authenticate": 'Basic realm="Capstone analyst"'})
    return expected_user


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid", allow_inf_nan=False)
    event_id: str = Field(min_length=1, max_length=128)
    timestamp: datetime
    source: str = Field(min_length=1, max_length=128)
    event_type: Literal["login_success", "file_read", "login_failure", "malware_alert", "privilege_change"]
    failed_attempts: int = Field(default=0, ge=0, le=1000000, strict=True)
    known_bad_ip: Literal[0, 1] = 0
    privileged_account: Literal[0, 1] = 0
    severity: float = Field(default=0.5, ge=0, le=1)
    business_impact: float = Field(default=0.5, ge=0, le=1)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest, analyst: str = Depends(require_analyst)) -> Dict[str, Any]:
    raw = request.model_dump(mode="json")
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
def events(limit: int = 50, analyst: str = Depends(require_analyst)):
    return {"events": list_analyses(limit=max(1, min(limit, 100)))}


@app.get("/", response_class=HTMLResponse)
def dashboard(analyst: str = Depends(require_analyst)) -> str:
    dashboard_path = Path(__file__).resolve().parents[1] / "dashboard" / "index.html"
    return dashboard_path.read_text(encoding="utf-8")
