
import json
import os
from collections import Counter

ALERT_FILE = "alerts.jsonl"

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                      ALERT REVIEW")
print("=" * 75)

# Check whether the alert file exists
if not os.path.exists(ALERT_FILE):
    print("\nAlert file not found:", ALERT_FILE)
    print("Run alert_logger.py first.")
    raise SystemExit

# Load saved alerts
alerts = []

with open(ALERT_FILE, "r", encoding="utf-8") as file:

    for line_number, line in enumerate(file, start=1):

        line = line.strip()

        if not line:
            continue

        try:
            alert = json.loads(line)
            alerts.append(alert)

        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON on line {line_number}")

# Handle an empty alert file
if not alerts:
    print("\nNo saved alerts are available to review.")

    input("\nPress Enter to exit...")
    raise SystemExit

# Summarize alert records
status_counts = Counter()
severity_counts = Counter()
type_counts = Counter()

for alert in alerts:
    status_counts[alert.get("status", "UNKNOWN")] += 1
    severity_counts[alert.get("severity", "UNKNOWN")] += 1
    type_counts[alert.get("alert_type", "UNKNOWN")] += 1

# Display summary
print("\n" + "=" * 75)
print("                    ALERT SUMMARY")
print("=" * 75)

print("Total saved alerts:", len(alerts))

print("\nBy status:")
for status, count in status_counts.items():
    print(f"  {status}: {count}")

print("\nBy severity:")
for severity, count in severity_counts.items():
    print(f"  {severity}: {count}")

print("\nBy alert type:")
for alert_type, count in type_counts.items():
    print(f"  {alert_type}: {count}")

# Display individual alert details
print("\n" + "=" * 75)
print("                    ALERT DETAILS")
print("=" * 75)

for number, alert in enumerate(alerts, start=1):

    print(f"\nAlert #{number}")
    print("-" * 75)

    print("Alert ID    :", alert.get("alert_id", "Unknown"))
    print("Time        :", alert.get("timestamp", "Unknown"))
    print("Type        :", alert.get("alert_type", "Unknown"))
    print("Process     :", alert.get("process", "Unknown"))
    print("Remote IP   :", alert.get("remote_ip", "Unknown"))
    print("Remote port :", alert.get("remote_port", "Unknown"))
    print("Severity    :", alert.get("severity", "Unknown"))
    print("Status      :", alert.get("status", "Unknown"))
    print("Description :", alert.get("description", "No description"))

    print("\nAnalyst reminder:")
    print("Verify the process and connection context before")
    print("deciding whether the alert indicates a real threat.")

print("\n" + "=" * 75)
print("                    REVIEW COMPLETE")
print("=" * 75)

input("\nPress Enter to exit...")