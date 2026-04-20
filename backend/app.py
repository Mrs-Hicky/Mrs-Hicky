from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="IoT Backend Starter")


class ReadingIn(BaseModel):
    device_id: str = Field(min_length=1)
    temperature_c: float
    humidity_pct: float
    timestamp: datetime


class Reading(ReadingIn):
    id: int


READINGS: List[Reading] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/readings", response_model=Reading, status_code=201)
def create_reading(payload: ReadingIn) -> Reading:
    reading = Reading(id=len(READINGS) + 1, **payload.model_dump())
    READINGS.append(reading)
    return reading


@app.get("/readings/latest", response_model=Reading)
def latest_reading() -> Reading:
    if not READINGS:
        raise HTTPException(status_code=404, detail="No readings available")
    return max(READINGS, key=lambda item: item.timestamp)


@app.get("/readings", response_model=list[Reading])
def list_readings(limit: int = 50) -> list[Reading]:
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be >= 1")
    return READINGS[-limit:]


@app.post("/dev/reset", status_code=204)
def reset_for_tests() -> None:
    """Utility endpoint for local demos/tests."""
    READINGS.clear()

