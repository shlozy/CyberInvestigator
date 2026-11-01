
import json

import pytest

from backend.storage.jsonl_store import (
    append_jsonl,
    read_jsonl,
    read_jsonl_with_fallback,
)


def test_append_and_read_record(tmp_path):
    file_path = tmp_path / "events.jsonl"
    record = {"event_type": "test", "count": 1}

    append_jsonl(file_path, record)

    assert read_jsonl(file_path) == [record]


def test_missing_file_returns_empty_list(tmp_path):
    file_path = tmp_path / "missing.jsonl"

    assert read_jsonl(file_path) == []


def test_malformed_line_is_skipped(tmp_path):
    file_path = tmp_path / "events.jsonl"

    file_path.write_text(
        '{"event_type": "valid"}\n'
        '{"event_type": invalid json}\n'
        '{"event_type": "another valid"}\n',
        encoding="utf-8",
    )

    records = read_jsonl(file_path)

    assert records == [
        {"event_type": "valid"},
        {"event_type": "another valid"},
    ]


def test_append_creates_parent_directories(tmp_path):
    file_path = tmp_path / "nested" / "events.jsonl"

    append_jsonl(file_path, {"status": "OPEN"})

    assert file_path.exists()
    assert read_jsonl(file_path) == [{"status": "OPEN"}]


def test_append_rejects_non_dictionary(tmp_path):
    file_path = tmp_path / "events.jsonl"

    with pytest.raises(TypeError):
        append_jsonl(file_path, ["not", "a", "dictionary"])

    assert not file_path.exists()


def test_fallback_reads_primary_when_it_exists(tmp_path):
    primary = tmp_path / "primary.jsonl"
    fallback = tmp_path / "fallback.jsonl"
    append_jsonl(primary, {"source": "primary"})
    append_jsonl(fallback, {"source": "fallback"})

    assert read_jsonl_with_fallback(primary, fallback) == [{"source": "primary"}]


def test_fallback_reads_fallback_when_primary_is_missing(tmp_path):
    primary = tmp_path / "missing.jsonl"
    fallback = tmp_path / "fallback.jsonl"
    append_jsonl(fallback, {"source": "fallback"})

    assert read_jsonl_with_fallback(primary, fallback) == [{"source": "fallback"}]


def test_fallback_returns_empty_list_when_both_are_missing(tmp_path):
    assert read_jsonl_with_fallback(
        tmp_path / "missing_a.jsonl",
        tmp_path / "missing_b.jsonl",
    ) == []


def test_empty_primary_does_not_fall_back(tmp_path):
    primary = tmp_path / "primary.jsonl"
    fallback = tmp_path / "fallback.jsonl"
    primary.write_text("", encoding="utf-8")
    append_jsonl(fallback, {"source": "fallback"})

    assert read_jsonl_with_fallback(primary, fallback) == []
