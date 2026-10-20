
import json
import os
import psutil
from datetime import datetime, timedelta

LOG_FILE = "network_events.jsonl"
BASELINE_FILE = "network_baseline.json"
TIME_WINDOW_SECONDS = 60

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 ALERT-TO-EVENT CORRELATOR")
print("=" * 75)

# Check required files
for filename in (LOG_FILE, BASELINE_FILE):
    if not os.path.exists(filename):
        print(f"\nRequired file not found: {filename}")
        print("Run the relevant collector/baseline builder first.")
        raise SystemExit

# Load the destination baseline
with open(BASELINE_FILE, "r", encoding="utf-8") as file:
    baseline_data = json.load(file)

network_baseline = baseline_data["network_baseline"]

# Load saved events
events = []

with open(LOG_FILE, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        try:
            event = json.loads(line)
            event["_time"] = datetime.fromisoformat(
                event["timestamp"]
            )
            events.append(event)

        except (json.JSONDecodeError, KeyError, ValueError):
            print(f"Skipping invalid log line: {line_number}")

# Collect current established connections
connections = psutil.net_connections(kind="inet")
current_relationships = set()

for connection in connections:

    if connection.status != "ESTABLISHED" or not connection.raddr:
        continue

    process_name = "Unknown"

    if connection.pid:
        try:
            process_name = psutil.Process(connection.pid).name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"

    current_relationships.add((
        process_name,
        connection.raddr.ip,
        connection.raddr.port
    ))

# Compare current relationships against the baseline
alerts = []
detection_time = datetime.now().astimezone()

for process_name, remote_ip, remote_port in current_relationships:

    known_destinations = network_baseline.get(process_name, [])

    known = any(
        destination.get("ip") == remote_ip
        and destination.get("port") == remote_port
        for destination in known_destinations
    )

    if not known:
        alerts.append({
            "time": detection_time,
            "process": process_name,
            "remote_ip": remote_ip,
            "remote_port": remote_port,
            "reason": "Destination relationship absent from baseline"
        })

# Find supporting observations around each alert
print("\nSaved events loaded:", len(events))
print("Current new-destination alerts:", len(alerts))

print("\n" + "=" * 75)
print("                    INVESTIGATION RESULTS")
print("=" * 75)

if not alerts:
    print("\nNo new-destination alerts generated in this snapshot.")

for number, alert in enumerate(alerts, start=1):

    start_time = alert["time"] - timedelta(
        seconds=TIME_WINDOW_SECONDS
    )
    end_time = alert["time"] + timedelta(
        seconds=TIME_WINDOW_SECONDS
    )

    related_events = []

    for event in events:

        same_process = (
            event.get("process") == alert["process"]
        )

        same_destination = (
            event.get("remote_ip") == alert["remote_ip"]
            and event.get("remote_port") == alert["remote_port"]
        )

        event_time = event["_time"]

        # Compare timezone-aware timestamps safely.
        if event_time.tzinfo is None:
            event_time = event_time.astimezone()

        within_window = start_time <= event_time <= end_time

        if same_process and same_destination and within_window:
            related_events.append(event)

    print(f"\nALERT #{number}")
    print("Detection time:", alert["time"].isoformat())
    print("Process       :", alert["process"])
    print("Remote IP     :", alert["remote_ip"])
    print("Remote port   :", alert["remote_port"])
    print("Reason        :", alert["reason"])
    print("Related events:", len(related_events))

    if related_events:
        for event in related_events:
            print(
                "  -", event["timestamp"],
                "| PID:", event.get("pid"),
                "| Status:", event.get("status")
            )
    else:
        print("  No matching observations found in the time window.")
        print("  This does not mean the connection is malicious.")

    print("-" * 75)

print("\nCorrelation complete.")

input("\nPress Enter to exit...")
