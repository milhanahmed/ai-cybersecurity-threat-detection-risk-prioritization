"""Explainable baseline risk-prioritization logic."""


def calculate_risk_score(severity: float, confidence: float, business_impact: float) -> float:
    values = [max(0.0, min(1.0, float(v))) for v in (severity, confidence, business_impact)]
    score = (0.40 * values[0] + 0.30 * values[1] + 0.30 * values[2]) * 100
    return round(score, 2)


def priority_from_score(score: float) -> str:
    if score >= 75:
        return "high"
    if score >= 50:
        return "medium"
    return "low"
