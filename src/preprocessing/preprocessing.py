"""Basic deterministic preprocessing utilities."""

from typing import Any, Dict, Iterable, List


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(event)
    for key, value in result.items():
        if isinstance(value, str):
            result[key] = value.strip()
    return result


def preprocess_events(events: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_event(event) for event in events]
