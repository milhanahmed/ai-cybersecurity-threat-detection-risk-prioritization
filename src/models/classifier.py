"""Replaceable interface for the AI threat-classification component."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ClassificationResult:
    label: str
    confidence: float


class ThreatClassifier:
    def predict(self, features: Dict[str, Any]) -> ClassificationResult:
        raise NotImplementedError("Trained classifier not integrated yet.")
