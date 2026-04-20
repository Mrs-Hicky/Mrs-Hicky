import os
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.store import SQLiteStore

app = FastAPI(title="IoT Backend Starter")


class ReadingIn(BaseModel):
    device_id: str = Field(min_length=1)
    temperature_c: float
    humidity_pct: float
    timestamp: datetime


class Reading(ReadingIn):
    id: int


def get_store() -> SQLiteStore:
    db_path = os.getenv("BACKEND_DB_PATH", "backend/data/readings.db")
    return SQLiteStore(db_path=db_path)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/readings", response_model=Reading, status_code=201)
def create_reading(payload: ReadingIn, store: SQLiteStore = Depends(get_store)) -> Reading:
    created = store.add_reading(**payload.model_dump())
    return Reading(**created.__dict__)


@app.get("/readings/latest", response_model=Reading)
def latest_reading(store: SQLiteStore = Depends(get_store)) -> Reading:
    latest = store.latest_reading()
    if latest is None:
        raise HTTPException(status_code=404, detail="No readings available")
    return Reading(**latest.__dict__)


@app.get("/readings", response_model=list[Reading])
def list_readings(limit: int = 50, store: SQLiteStore = Depends(get_store)) -> list[Reading]:
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be >= 1")
    readings = store.list_readings(limit=limit)
    return [Reading(**item.__dict__) for item in readings]


@app.post("/dev/reset", status_code=204)
def reset_for_tests(store: SQLiteStore = Depends(get_store)) -> None:
    """Utility endpoint for local demos/tests."""
    store.clear()
