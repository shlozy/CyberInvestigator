
import json
from pathlib import Path


def read_jsonl(file_path):
    """Read valid JSON object records from a JSONL file."""
    path = Path(file_path)

    if not path.exists():
        return []

    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(record, dict):
                records.append(record)

    return records


def read_jsonl_with_fallback(primary_path, fallback_path):
    """Read the primary file if it exists, otherwise the fallback file.

    An existing primary file is always used, even when it is empty.
    """
    primary = Path(primary_path)

    if primary.exists():
        return read_jsonl(primary)

    return read_jsonl(fallback_path)


def append_jsonl(file_path, record):
    """Append one dictionary as a JSONL record."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(record, ensure_ascii=False) + "\n"
        )
