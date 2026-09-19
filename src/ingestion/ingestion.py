"""Input validation and ingestion boundary for cybersecurity events."""

from typing import Any, Dict, Iterable, List

REQUIRED_FIELDS = {"event_id", "timestamp", "source", "event_type"}


def validate_event(event: Dict[str, Any]) -> bool:
    return REQUIRED_FIELDS.issubset(event.keys())


def ingest_events(events: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [event for event in events if validate_event(event)]
