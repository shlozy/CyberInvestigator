from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.storage import paths
from backend.storage.jsonl_store import read_jsonl_with_fallback

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

PROJECT_ROOT = paths.PROJECT_ROOT
NEW_ALERTS_FILE = paths.ALERTS_FILE
LEGACY_ALERTS_FILE = paths.LEGACY_ALERTS_FILE
NEW_NETWORK_EVENTS_FILE = paths.NETWORK_EVENTS_FILE
LEGACY_NETWORK_EVENTS_FILE = paths.LEGACY_NETWORK_EVENTS_FILE


def read_saved_alerts():
    """Read saved alerts without modifying the original file."""
    return read_jsonl_with_fallback(NEW_ALERTS_FILE, LEGACY_ALERTS_FILE)


def read_saved_network_events():
    """Read saved network events without modifying the original file."""
    return read_jsonl_with_fallback(
        NEW_NETWORK_EVENTS_FILE,
        LEGACY_NETWORK_EVENTS_FILE,
    )


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


@app.get("/network-events")
def get_network_events():
    """Return saved network events exactly as they were recorded."""
    events = read_saved_network_events()

    return {
        "total": len(events),
        "events": events,
    }
