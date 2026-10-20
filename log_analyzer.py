
import json
import os
from collections import Counter

LOG_FILE = "network_events.jsonl"

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                    SECURITY LOG ANALYZER")
print("=" * 75)

# Check whether the log file exists
if not os.path.exists(LOG_FILE):
    print("\nLog file not found:", LOG_FILE)
    print("Run network_event_logger.py first.")
    input("\nPress Enter to exit...")
    raise SystemExit

events = []

# Read previously recorded events
with open(LOG_FILE, "r", encoding="utf-8") as file:

    for line_number, line in enumerate(file, start=1):

        line = line.strip()

        if not line:
            continue

        try:
            event = json.loads(line)
            events.append(event)

        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON on line {line_number}")

# Summarize the records
process_counts = Counter()
port_counts = Counter()
status_counts = Counter()

for event in events:
    process_counts[event.get("process", "Unknown")] += 1
    port_counts[event.get("remote_port", "Unknown")] += 1
    status_counts[event.get("status", "Unknown")] += 1

print("\n" + "=" * 75)
print("                    EVENT SUMMARY")
print("=" * 75)

print("\nTotal valid events:", len(events))

print("\nEvents by process:")
for process, count in process_counts.most_common():
    print(f"  {process}: {count}")

print("\nEvents by remote port:")
for port, count in port_counts.most_common():
    print(f"  Port {port}: {count}")

print("\nEvents by status:")
for status, count in status_counts.most_common():
    print(f"  {status}: {count}")

if events:
    print("\nFirst recorded event:", events[0].get("timestamp", "Unknown"))
    print("Last recorded event :", events[-1].get("timestamp", "Unknown"))

print("\nLog analysis complete.")

input("\nPress Enter to exit...")