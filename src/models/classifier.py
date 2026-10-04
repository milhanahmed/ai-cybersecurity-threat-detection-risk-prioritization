"""Trainable baseline threat classifier for the capstone prototype."""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


@dataclass
class ClassificationResult:
    label: str
    confidence: float


class ThreatClassifier:
    """Small supervised classifier that accepts dictionary-based security features."""

    def __init__(self) -> None:
        self.pipeline = Pipeline(
            [
                ("vectorizer", DictVectorizer(sparse=True)),
                ("classifier", LogisticRegression(max_iter=500, random_state=42)),
            ]
        )
        self._is_fitted = False

    def fit(self, features: Iterable[Dict[str, Any]], labels: Iterable[str]) -> "ThreatClassifier":
        feature_rows: List[Dict[str, Any]] = list(features)
        target_labels: List[str] = list(labels)
        if len(feature_rows) < 2 or len(set(target_labels)) < 2:
            raise ValueError("Training requires at least two samples and two classes.")
        self.pipeline.fit(feature_rows, target_labels)
        self._is_fitted = True
        return self

    def predict(self, features: Dict[str, Any]) -> ClassificationResult:
        if not self._is_fitted:
            raise RuntimeError("Classifier must be fitted before prediction.")
        probabilities = self.pipeline.predict_proba([features])[0]
        classes = self.pipeline.named_steps["classifier"].classes_
        best_index = int(probabilities.argmax())
        return ClassificationResult(
            label=str(classes[best_index]),
            confidence=round(float(probabilities[best_index]), 4),
        )
