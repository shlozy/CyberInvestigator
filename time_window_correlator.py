
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

LOG_FILE = "network_events.jsonl"
WINDOW_SECONDS = 30

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 TIME-WINDOW CORRELATOR")
print("=" * 75)

if not os.path.exists(LOG_FILE):
    print("\nLog file not found. Run network_event_logger.py first.")
    raise SystemExit

events = []

# Read saved events
with open(LOG_FILE, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        try:
            event = json.loads(line)
            event["_time"] = datetime.fromisoformat(
                event["timestamp"]
            )
            events.append(event)

        except (json.JSONDecodeError, KeyError, ValueError):
            print(f"Skipping invalid event on line {line_number}")

# Group by process and remote IP
groups = defaultdict(list)

for event in events:
    key = (
        event.get("process", "Unknown"),
        event.get("remote_ip", "Unknown")
    )
    groups[key].append(event)

print("\nValid events:", len(events))
print("Time window:", WINDOW_SECONDS, "seconds")

cluster_number = 0

print("\n" + "=" * 75)
print("                    CORRELATION RESULTS")
print("=" * 75)

for (process, remote_ip), group_events in groups.items():

    # Put observations in chronological order
    group_events.sort(key=lambda event: event["_time"])

    clusters = []
    current_cluster = []

    for event in group_events:

        if not current_cluster:
            current_cluster.append(event)
            continue

        previous_time = current_cluster[-1]["_time"]
        current_time = event["_time"]

        gap = (current_time - previous_time).total_seconds()

        if gap <= WINDOW_SECONDS:
            current_cluster.append(event)

        else:
            clusters.append(current_cluster)
            current_cluster = [event]

    if current_cluster:
        clusters.append(current_cluster)

    # Display each cluster
    for cluster in clusters:

        cluster_number += 1

        start_time = cluster[0]["_time"]
        end_time = cluster[-1]["_time"]

        print(f"\nCluster #{cluster_number}")
        print("Process       :", process)
        print("Remote IP     :", remote_ip)
        print("Observations  :", len(cluster))
        print("First observed:", start_time.isoformat())
        print("Last observed :", end_time.isoformat())

        if len(cluster) > 1:
            print("Relationship  : Repeated observations within the time window")
        else:
            print("Relationship  : Single observation")

        print("-" * 75)

print("\nTotal correlation clusters:", cluster_number)
print("Time-window correlation complete.")

input("\nPress Enter to exit...")
