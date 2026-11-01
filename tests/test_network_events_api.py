
import json

import pytest
from fastapi.testclient import TestClient

from backend.api import main
from backend.api.main import app

client = TestClient(app)

SAMPLE_EVENT = {
    "timestamp": "2026-10-09T23:18:03+05:30",
    "event_type": "network_connection_observed",
    "process": "chrome.exe",
    "pid": 18672,
    "local_ip": "192.168.1.5",
    "local_port": 64699,
    "remote_ip": "142.250.183.14",
    "remote_port": 443,
    "status": "ESTABLISHED",
}


@pytest.fixture
def event_files(tmp_path, monkeypatch):
    """Point the API at temporary event files instead of real data."""
    new_file = tmp_path / "data" / "network_events.jsonl"
    legacy_file = tmp_path / "network_events.jsonl"

    monkeypatch.setattr(main, "NEW_NETWORK_EVENTS_FILE", new_file)
    monkeypatch.setattr(main, "LEGACY_NETWORK_EVENTS_FILE", legacy_file)

    return new_file, legacy_file


def write_lines(file_path, lines):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("".join(line + "\n" for line in lines), encoding="utf-8")


def test_returns_saved_events_in_file_order(event_files):
    new_file, _ = event_files
    second_event = {**SAMPLE_EVENT, "process": "Code.exe", "pid": 4348}
    write_lines(new_file, [json.dumps(SAMPLE_EVENT), json.dumps(second_event)])

    response = client.get("/network-events")

    assert response.status_code == 200
    assert response.json() == {
        "total": 2,
        "events": [SAMPLE_EVENT, second_event],
    }


def test_missing_files_return_empty_result(event_files):
    response = client.get("/network-events")

    assert response.status_code == 200
    assert response.json() == {"total": 0, "events": []}


def test_malformed_and_non_object_lines_are_skipped(event_files):
    new_file, _ = event_files
    write_lines(
        new_file,
        [
            json.dumps(SAMPLE_EVENT),
            '{"process": broken json}',
            "[1, 2, 3]",
            '"just a string"',
            "",
            json.dumps({**SAMPLE_EVENT, "pid": 99}),
        ],
    )

    response = client.get("/network-events")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert [event["pid"] for event in body["events"]] == [18672, 99]


def test_legacy_file_is_used_when_new_file_is_missing(event_files):
    _, legacy_file = event_files
    write_lines(legacy_file, [json.dumps(SAMPLE_EVENT)])

    response = client.get("/network-events")

    assert response.json() == {"total": 1, "events": [SAMPLE_EVENT]}


def test_new_file_is_preferred_over_legacy_file(event_files):
    new_file, legacy_file = event_files
    new_event = {**SAMPLE_EVENT, "process": "new.exe"}
    write_lines(new_file, [json.dumps(new_event)])
    write_lines(legacy_file, [json.dumps(SAMPLE_EVENT)])

    response = client.get("/network-events")

    assert response.json() == {"total": 1, "events": [new_event]}


def test_empty_new_file_does_not_fall_back_to_legacy(event_files):
    new_file, legacy_file = event_files
    write_lines(new_file, [])
    write_lines(legacy_file, [json.dumps(SAMPLE_EVENT)])

    response = client.get("/network-events")

    assert response.json() == {"total": 0, "events": []}


def test_partial_records_are_returned_unchanged(event_files):
    new_file, _ = event_files
    partial_events = [
        {**SAMPLE_EVENT, "pid": None, "process": "Unknown"},
        {"timestamp": "2026-10-09T23:20:45+05:30", "remote_ip": "1.1.1.1"},
        {**SAMPLE_EVENT, "extra_field": "kept as-is"},
    ]
    write_lines(new_file, [json.dumps(event) for event in partial_events])

    response = client.get("/network-events")

    assert response.json()["events"] == partial_events


def test_reading_events_does_not_modify_the_file(event_files):
    new_file, _ = event_files
    write_lines(new_file, [json.dumps(SAMPLE_EVENT), "not json"])
    original_bytes = new_file.read_bytes()

    client.get("/network-events")

    assert new_file.read_bytes() == original_bytes


def test_response_has_consistent_structure(event_files):
    new_file, _ = event_files
    write_lines(new_file, [json.dumps(SAMPLE_EVENT)] * 3)

    body = client.get("/network-events").json()

    assert set(body.keys()) == {"total", "events"}
    assert isinstance(body["events"], list)
    assert body["total"] == len(body["events"])
