# Architecture overview

## System flow

1. Device reads sensor values on a schedule.
2. Device sends data to backend API.
3. Backend validates and stores readings.
4. Dashboard/CLI retrieves data for display.

## Non-functional goals

- Simplicity first.
- Observable failures (clear logs).
- Reproducible local setup.

## Future enhancements

- Device authentication.
- Persistent database and migrations.
- Alerting for out-of-range thresholds.
- Basic load and resilience testing.
