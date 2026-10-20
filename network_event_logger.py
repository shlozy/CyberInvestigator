
import psutil
import json
import time
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                   NETWORK EVENT LOGGER")
print("=" * 75)

SAMPLES = 6
INTERVAL = 5
LOG_FILE = "network_events.jsonl"

print(f"\nCollecting {SAMPLES} observations...")
print(f"Saving events to: {LOG_FILE}\n")

total_events = 0

with open(LOG_FILE, "a", encoding="utf-8") as file:

    for sample in range(1, SAMPLES + 1):

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
                "status": connection.status
            }

            file.write(json.dumps(event) + "\n")
            total_events += 1

        file.flush()

        print(
            f"Observation {sample}/{SAMPLES} completed. "
            f"Events recorded so far: {total_events}"
        )

        if sample < SAMPLES:
            time.sleep(INTERVAL)

print("\n" + "=" * 75)
print("                    COLLECTION COMPLETE")
print("=" * 75)

print("Total events recorded:", total_events)
print("Log file:", LOG_FILE)

input("\nPress Enter to exit...")