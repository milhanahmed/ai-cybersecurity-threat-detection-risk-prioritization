"""Evaluate classifier accuracy and API processing latency for the integrated prototype."""

import json
import os
import statistics
import time

os.environ.setdefault("CYBER_DB_PATH", "data/evaluation.db")

from fastapi.testclient import TestClient
from src.api.app import app, classifier

EVAL_CASES = [
    ({"event_type": "login_success", "failed_attempts": 0, "known_bad_ip": 0, "privileged_account": 0}, "benign"),
    ({"event_type": "file_read", "failed_attempts": 0, "known_bad_ip": 0, "privileged_account": 0}, "benign"),
    ({"event_type": "login_failure", "failed_attempts": 1, "known_bad_ip": 0, "privileged_account": 0}, "benign"),
    ({"event_type": "login_failure", "failed_attempts": 10, "known_bad_ip": 1, "privileged_account": 1}, "suspicious"),
    ({"event_type": "malware_alert", "failed_attempts": 0, "known_bad_ip": 1, "privileged_account": 0}, "suspicious"),
    ({"event_type": "privilege_change", "failed_attempts": 2, "known_bad_ip": 0, "privileged_account": 1}, "suspicious"),
]

correct = sum(classifier.predict(features).label == expected for features, expected in EVAL_CASES)
accuracy = correct / len(EVAL_CASES)

client = TestClient(app)
latencies_ms = []
for i in range(30):
    payload = {
        "event_id": f"PERF-{i}",
        "timestamp": "2026-10-06T12:00:00Z",
        "source": "evaluation-client",
        "event_type": "login_failure",
        "failed_attempts": 8,
        "known_bad_ip": 1,
        "privileged_account": 1,
        "severity": 0.9,
        "business_impact": 0.8,
    }
    start = time.perf_counter()
    response = client.post("/analyze", json=payload)
    response.raise_for_status()
    latencies_ms.append((time.perf_counter() - start) * 1000)

results = {
    "classification_accuracy": round(accuracy, 4),
    "requests_measured": len(latencies_ms),
    "mean_latency_ms": round(statistics.mean(latencies_ms), 3),
    "median_latency_ms": round(statistics.median(latencies_ms), 3),
    "approx_throughput_requests_per_second": round(1000 / statistics.mean(latencies_ms), 2),
}
print(json.dumps(results, indent=2))
