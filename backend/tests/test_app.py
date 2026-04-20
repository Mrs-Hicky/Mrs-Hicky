from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def setup_function() -> None:
    client.post('/dev/reset')


def test_health_endpoint() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_create_and_fetch_latest_reading() -> None:
    payload = {
        'device_id': 'esp32-lab-01',
        'temperature_c': 24.6,
        'humidity_pct': 43.2,
        'timestamp': '2026-04-20T12:00:00Z',
    }

    create = client.post('/readings', json=payload)
    assert create.status_code == 201
    body = create.json()
    assert body['id'] == 1

    latest = client.get('/readings/latest')
    assert latest.status_code == 200
    assert latest.json()['device_id'] == payload['device_id']


def test_list_readings_limit() -> None:
    for idx in range(3):
        payload = {
            'device_id': f'esp32-{idx}',
            'temperature_c': 20 + idx,
            'humidity_pct': 40 + idx,
            'timestamp': f'2026-04-20T12:00:0{idx}Z',
        }
        client.post('/readings', json=payload)

    response = client.get('/readings', params={'limit': 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['device_id'] == 'esp32-1'
    assert data[1]['device_id'] == 'esp32-2'
