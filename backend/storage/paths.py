
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

NETWORK_EVENTS_FILE = DATA_DIR / "network_events.jsonl"
ALERTS_FILE = DATA_DIR / "alerts.jsonl"
NETWORK_BASELINE_FILE = DATA_DIR / "network_baseline.json"
PROCESS_BASELINE_FILE = DATA_DIR / "baseline.json"
