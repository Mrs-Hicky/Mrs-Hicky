# Backend module

This folder contains the API service that receives and stores telemetry.

## Recommended first milestone

- Create `POST /readings` endpoint.
- Validate payload shape and required fields.
- Store data in memory first, then move to SQLite.

## Suggested payload

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

- Storage is currently in-memory for simplicity.
- Next step: move storage to SQLite and add persistence tests.
## Suggested next step

Add `GET /readings/latest` and `GET /readings?limit=50`.
