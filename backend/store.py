import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ReadingRecord:
    id: int
    device_id: str
    temperature_c: float
    humidity_pct: float
    timestamp: datetime


class SQLiteStore:
    def __init__(self, db_path: str = "backend/data/readings.db") -> None:
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    temperature_c REAL NOT NULL,
                    humidity_pct REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_reading(
        self,
        *,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        timestamp: datetime,
    ) -> ReadingRecord:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO readings (device_id, temperature_c, humidity_pct, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (device_id, temperature_c, humidity_pct, timestamp.isoformat()),
            )
            conn.commit()
            reading_id = int(cursor.lastrowid)
        return ReadingRecord(
            id=reading_id,
            device_id=device_id,
            temperature_c=temperature_c,
            humidity_pct=humidity_pct,
            timestamp=timestamp,
        )

    def list_readings(self, *, limit: int = 50) -> list[ReadingRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, device_id, temperature_c, humidity_pct, timestamp
                FROM readings
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        rows = list(reversed(rows))
        return [self._to_record(row) for row in rows]

    def latest_reading(self) -> ReadingRecord | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, device_id, temperature_c, humidity_pct, timestamp
                FROM readings
                ORDER BY timestamp DESC, id DESC
                LIMIT 1
                """
            ).fetchone()
        if row is None:
            return None
        return self._to_record(row)

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM readings")
            conn.commit()

    @staticmethod
    def _to_record(row: sqlite3.Row) -> ReadingRecord:
        return ReadingRecord(
            id=row["id"],
            device_id=row["device_id"],
            temperature_c=row["temperature_c"],
            humidity_pct=row["humidity_pct"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
        )
