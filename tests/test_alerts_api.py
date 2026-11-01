
import json

import pytest
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


@pytest.fixture
def alert_files(tmp_path, monkeypatch):
    """Point the API at temporary alert files instead of real data."""
    from backend.api import main

    new_file = tmp_path / "data" / "alerts.jsonl"
    legacy_file = tmp_path / "alerts.jsonl"

    monkeypatch.setattr(main, "NEW_ALERTS_FILE", new_file)
    monkeypatch.setattr(main, "LEGACY_ALERTS_FILE", legacy_file)

    return new_file, legacy_file


def write_alerts(file_path, lines):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("".join(line + "\n" for line in lines), encoding="utf-8")


def test_alerts_use_legacy_file_when_new_file_is_missing(alert_files):
    _, legacy_file = alert_files
    write_alerts(legacy_file, [json.dumps({"alert_type": "legacy"})])

    response = client.get("/alerts")

    assert response.json() == {
        "total": 1,
        "alerts": [{"alert_type": "legacy"}],
    }


def test_alerts_prefer_new_file_over_legacy_file(alert_files):
    new_file, legacy_file = alert_files
    write_alerts(new_file, [json.dumps({"alert_type": "new"})])
    write_alerts(legacy_file, [json.dumps({"alert_type": "legacy"})])

    response = client.get("/alerts")

    assert response.json() == {
        "total": 1,
        "alerts": [{"alert_type": "new"}],
    }


def test_alerts_skip_malformed_lines(alert_files):
    new_file, _ = alert_files
    write_alerts(
        new_file,
        [
            json.dumps({"alert_type": "valid"}),
            "{broken",
            "[1, 2]",
        ],
    )

    response = client.get("/alerts")

    assert response.json() == {
        "total": 1,
        "alerts": [{"alert_type": "valid"}],
    }
