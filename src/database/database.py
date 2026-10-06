"""SQLite persistence for analyzed cybersecurity events."""

import os
import sqlite3
from typing import Any, Dict, List

DB_PATH = os.getenv("CYBER_DB_PATH", "data/cybersecurity.db")


def _connect() -> sqlite3.Connection:
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyzed_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                event_type TEXT NOT NULL,
                predicted_label TEXT NOT NULL,
                confidence REAL NOT NULL,
                risk_score REAL NOT NULL,
                priority TEXT NOT NULL
            )
            """
        )


def save_analysis(record: Dict[str, Any]) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO analyzed_events
            (event_id, timestamp, source, event_type, predicted_label, confidence, risk_score, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["event_id"], record["timestamp"], record["source"], record["event_type"],
                record["predicted_label"], record["confidence"], record["risk_score"], record["priority"],
            ),
        )


def list_analyses(limit: int = 50) -> List[Dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM analyzed_events ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]
