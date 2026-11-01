from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

from fastapi import FastAPI

app = FastAPI(
    title="Cyber Investigator API",
    description="API for the Cyber Investigator investigation platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NEW_ALERTS_FILE = PROJECT_ROOT / "data" / "alerts.jsonl"
LEGACY_ALERTS_FILE = PROJECT_ROOT / "alerts.jsonl"


def read_saved_alerts():
    """Read saved alerts without modifying the original file."""
    if NEW_ALERTS_FILE.exists():
        alerts_file = NEW_ALERTS_FILE
    else:
        alerts_file = LEGACY_ALERTS_FILE

    if not alerts_file.exists():
        return []

    alerts = []

    with alerts_file.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                alert = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(alert, dict):
                alerts.append(alert)

    return alerts


@app.get("/health")
def health_check():
    """Confirm that the API is running."""
    return {
        "status": "healthy",
        "service": "Cyber Investigator API",
    }


@app.get("/alerts")
def get_alerts():
    """Return saved security alerts."""
    alerts = read_saved_alerts()

    return {
        "total": len(alerts),
        "alerts": alerts,
    }
