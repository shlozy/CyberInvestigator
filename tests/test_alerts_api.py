
from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_alerts_endpoint_returns_expected_structure(monkeypatch):
    from backend.api import main

    monkeypatch.setattr(
        main,
        "NEW_ALERTS_FILE",
        main.PROJECT_ROOT / "test_alerts_file_that_does_not_exist.jsonl",
    )
    monkeypatch.setattr(
        main,
        "LEGACY_ALERTS_FILE",
        main.PROJECT_ROOT / "test_alerts_file_that_does_not_exist.jsonl",
    )

    response = client.get("/alerts")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "alerts": [],
    }
