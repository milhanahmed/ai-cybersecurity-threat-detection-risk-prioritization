from src.ingestion.ingestion import ingest_events, validate_event
from src.models.classifier import ThreatClassifier
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


def test_risk_score_clamps_out_of_range_values():
    score = calculate_risk_score(2, -1, 0.5)
    assert score == 55.0
    assert priority_from_score(score) == "medium"


def test_classifier_requires_training():
    classifier = ThreatClassifier()
    try:
        classifier.predict({"failed_logins": 8, "event_type": "login"})
        assert False, "Expected RuntimeError for an unfitted classifier"
    except RuntimeError:
        assert True


def test_classifier_fit_and_predict():
    features = [
        {"event_type": "login", "failed_logins": 0, "severity": 0.1},
        {"event_type": "login", "failed_logins": 1, "severity": 0.2},
        {"event_type": "file_access", "failed_logins": 0, "severity": 0.1},
        {"event_type": "login", "failed_logins": 8, "severity": 0.9},
        {"event_type": "login", "failed_logins": 10, "severity": 1.0},
        {"event_type": "malware", "failed_logins": 0, "severity": 1.0},
    ]
    labels = ["normal", "normal", "normal", "suspicious", "suspicious", "suspicious"]

    classifier = ThreatClassifier().fit(features, labels)
    result = classifier.predict({"event_type": "login", "failed_logins": 9, "severity": 0.95})

    assert result.label == "suspicious"
    assert 0.5 <= result.confidence <= 1.0
