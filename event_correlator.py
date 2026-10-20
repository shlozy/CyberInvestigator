
import json
import os
from collections import defaultdict
from datetime import datetime

LOG_FILE = "network_events.jsonl"

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                    EVENT CORRELATOR")
print("=" * 75)

if not os.path.exists(LOG_FILE):
    print("\nLog file not found. Run network_event_logger.py first.")
    raise SystemExit

events = []

with open(LOG_FILE, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):

        try:
            event = json.loads(line)

            timestamp = datetime.fromisoformat(event["timestamp"])

            event["_parsed_time"] = timestamp
            events.append(event)

        except (json.JSONDecodeError, KeyError, ValueError):
            print(f"Skipping invalid event on line {line_number}")

# Group observations by process and remote port
groups = defaultdict(list)

for event in events:

    process = event.get("process", "Unknown")
    remote_port = event.get("remote_port", "Unknown")

    key = (process, remote_port)
    groups[key].append(event)

print("\nTotal valid events:", len(events))
print("Correlation groups:", len(groups))

print("\n" + "=" * 75)
print("                    CORRELATION RESULTS")
print("=" * 75)

for (process, remote_port), group_events in groups.items():

    times = [
        event["_parsed_time"]
        for event in group_events
    ]

    first_seen = min(times)
    last_seen = max(times)

    duration = (last_seen - first_seen).total_seconds()

    print("\nProcess     :", process)
    print("Remote port :", remote_port)
    print("Observations:", len(group_events))
    print("First seen  :", first_seen.isoformat())
    print("Last seen   :", last_seen.isoformat())
    print("Time span   :", duration, "seconds")

    if len(group_events) > 1:
        print("Relationship: Repeated observations")
    else:
        print("Relationship: Single observation")

    print("-" * 75)

print("\nEvent correlation complete.")

input("\nPress Enter to exit...")