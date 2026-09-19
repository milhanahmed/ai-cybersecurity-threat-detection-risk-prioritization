"""Minimal API boundary for the capstone prototype."""

from fastapi import FastAPI
from pydantic import BaseModel

from src.risk_scoring.risk_score import calculate_risk_score, priority_from_score

app = FastAPI(title="AI Cybersecurity Threat Detection and Risk Prioritization")


class RiskRequest(BaseModel):
    severity: float
    confidence: float
    business_impact: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/risk-score")
def risk_score(request: RiskRequest):
    score = calculate_risk_score(request.severity, request.confidence, request.business_impact)
    return {"risk_score": score, "priority": priority_from_score(score)}
