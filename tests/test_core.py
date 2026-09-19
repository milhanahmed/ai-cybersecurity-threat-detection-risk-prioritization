from src.ingestion.ingestion import ingest_events, validate_event
from src.preprocessing.preprocessing import normalize_event
from src.risk_scoring.risk_score import calculate_risk_score, priority_from_score


def test_validate_event():
    assert validate_event({"event_id": "E1", "timestamp": "2026-01-01T00:00:00Z", "source": "test", "event_type": "login"})


def test_ingestion_rejects_invalid_event():
    assert ingest_events([{"event_id": "E1"}]) == []


def test_normalization():
    assert normalize_event({"source": " test "})["source"] == "test"


def test_risk_score_and_priority():
    score = calculate_risk_score(1, 1, 1)
    assert score == 100
    assert priority_from_score(score) == "high"
