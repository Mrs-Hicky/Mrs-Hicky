# Backend module

This folder contains a minimal FastAPI service that receives and stores telemetry in SQLite.

## Implemented endpoints

- `GET /health` → basic health check
- `POST /readings` → ingest one reading
- `GET /readings/latest` → fetch most recent reading by timestamp
- `GET /readings?limit=50` → list recent readings

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

## Data storage

- Default database path: `backend/data/readings.db`
- Override path for local/dev/tests with `BACKEND_DB_PATH`

## Example payload

```json
{
  "device_id": "esp32-lab-01",
  "temperature_c": 24.6,
  "humidity_pct": 43.2,
  "timestamp": "2026-04-20T12:00:00Z"
}
```

## Run tests

```bash
pytest backend/tests -q
```

## Notes

- Persistence is now SQLite-backed.
- Next step: add migration tooling and device authentication.
