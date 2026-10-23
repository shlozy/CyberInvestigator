
import json
import time
from datetime import datetime
from pathlib import Path

import psutil

from backend.storage.paths import PROJECT_ROOT

SAMPLES = 6
INTERVAL = 5

# Keep the existing log location while other scripts
# are still being migrated.
LOG_FILE = PROJECT_ROOT / "network_events.jsonl"


def collect_events(samples=SAMPLES, interval=INTERVAL, log_file=LOG_FILE):
    """Collect established network connections and save them as JSONL."""

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    total_events = 0

    print(f"\nCollecting {samples} observations...")
    print(f"Saving events to: {log_file}")

    with log_file.open("a", encoding="utf-8") as file:
        for sample in range(1, samples + 1):
            connections = psutil.net_connections(kind="inet")

            timestamp = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )

            for connection in connections:
                if connection.status != "ESTABLISHED":
                    continue

                if not connection.raddr:
                    continue

                process_name = "Unknown"

                if connection.pid:
                    try:
                        process_name = psutil.Process(
                            connection.pid
                        ).name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = "Unknown"

                event = {
                    "timestamp": timestamp,
                    "event_type": "network_connection_observed",
                    "process": process_name,
                    "pid": connection.pid,
                    "local_ip": connection.laddr.ip,
                    "local_port": connection.laddr.port,
                    "remote_ip": connection.raddr.ip,
                    "remote_port": connection.raddr.port,
                    "status": connection.status,
                }

                file.write(json.dumps(event) + "\n")
                total_events += 1

            file.flush()

            print(
                f"Observation {sample}/{samples} completed. "
                f"Events recorded so far: {total_events}"
            )

            if sample < samples:
                time.sleep(interval)

    print(f"\nCollection complete. Events recorded: {total_events}")
    print(f"Log file: {log_file}")

    return total_events


def main():
    """Run the collector as a standalone program."""
    print("=" * 75)
    print("                    CYBER INVESTIGATOR")
    print("                   NETWORK EVENT LOGGER")
    print("=" * 75)

    collect_events()
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
