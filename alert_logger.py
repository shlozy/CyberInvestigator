
import json
import os
import psutil
from datetime import datetime

BASELINE_FILE = "network_baseline.json"
ALERT_FILE = "alerts.jsonl"

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                      ALERT LOGGER")
print("=" * 75)

# Load the existing network baseline
if not os.path.exists(BASELINE_FILE):
    print("\nBaseline file not found:", BASELINE_FILE)
    print("Run build_network_baseline.py first.")
    raise SystemExit

with open(BASELINE_FILE, "r", encoding="utf-8") as file:
    baseline_data = json.load(file)

network_baseline = baseline_data["network_baseline"]

print("\nBaseline loaded successfully.")

# Collect current connections
connections = psutil.net_connections(kind="inet")

current_relationships = set()

for connection in connections:

    if connection.status != "ESTABLISHED":
        continue

    if not connection.raddr:
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

# Compare against baseline and create alerts
new_alerts = []
detection_time = datetime.now().astimezone().isoformat(
    timespec="seconds"
)

for process_name, remote_ip, remote_port in current_relationships:

    known_destinations = network_baseline.get(process_name, [])

    destination_known = any(
        item.get("ip") == remote_ip
        and item.get("port") == remote_port
        for item in known_destinations
    )

    if not destination_known:

        alert = {
            "alert_id": (
                f"{detection_time}|{process_name}|"
                f"{remote_ip}|{remote_port}"
            ),
            "timestamp": detection_time,
            "alert_type": "NEW_DESTINATION",
            "process": process_name,
            "remote_ip": remote_ip,
            "remote_port": remote_port,
            "severity": "LOW",
            "status": "OPEN",
            "description": (
                "Process-to-destination relationship "
                "was absent from the saved baseline."
            )
        }

        new_alerts.append(alert)

# Append alerts to the persistent log
with open(ALERT_FILE, "a", encoding="utf-8") as file:

    for alert in new_alerts:
        file.write(json.dumps(alert) + "\n")

print("\n" + "=" * 75)
print("                    ALERT RESULTS")
print("=" * 75)

print("Current relationships checked:", len(current_relationships))
print("New alerts generated:", len(new_alerts))

if new_alerts:
    for alert in new_alerts:
        print("\nAlert ID   :", alert["alert_id"])
        print("Process    :", alert["process"])
        print("Remote IP  :", alert["remote_ip"])
        print("Remote port:", alert["remote_port"])
        print("Severity   :", alert["severity"])
        print("Status     :", alert["status"])
else:
    print("\nNo new-destination alerts generated in this run.")

print("\nAlerts saved to:", ALERT_FILE)
print("Previous alert records have been preserved.")

input("\nPress Enter to exit...")
