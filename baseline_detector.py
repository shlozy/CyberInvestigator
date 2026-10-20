import psutil
import json
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 BASELINE DETECTOR")
print("=" * 75)


# --------------------------------------------------
# STEP 1: LOAD BASELINE
# --------------------------------------------------

with open("baseline.json", "r") as file:
    baseline_data = json.load(file)

baseline = baseline_data["process_baseline"]

print("\nBaseline loaded successfully.")
print("Baseline created at:", baseline_data["created_at"])


# --------------------------------------------------
# STEP 2: COLLECT CURRENT NETWORK ACTIVITY
# --------------------------------------------------

print("\nCollecting current network activity...\n")

connections = psutil.net_connections(kind="inet")

current_connections = {}


for connection in connections:

    if connection.status != "ESTABLISHED":
        continue

    if not connection.raddr:
        continue

    process_name = "Unknown"

    if connection.pid:

        try:
            process = psutil.Process(connection.pid)
            process_name = process.name()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"


    if process_name not in current_connections:
        current_connections[process_name] = 0

    current_connections[process_name] += 1


# --------------------------------------------------
# STEP 3: COMPARE WITH BASELINE
# --------------------------------------------------

anomalies = []


for process, current_count in current_connections.items():

    if process in baseline:

        normal_maximum = baseline[process]["maximum"]

        if current_count > normal_maximum:

            anomaly = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "process": process,
                "current_connections": current_count,
                "normal_maximum": normal_maximum,
                "rule": "Connection count above baseline",
                "severity": "MEDIUM"
            }

            anomalies.append(anomaly)


# --------------------------------------------------
# STEP 4: DISPLAY RESULTS
# --------------------------------------------------

print("=" * 75)
print("                    CURRENT ACTIVITY")
print("=" * 75)

for process, count in current_connections.items():

    print(f"{process}: {count}")


print("\n" + "=" * 75)
print("                    DETECTION RESULTS")
print("=" * 75)


if len(anomalies) == 0:

    print("\nNo baseline anomalies detected.")

else:

    for anomaly in anomalies:

        print("\n🚨 ANOMALY DETECTED")

        print("Time              :", anomaly["time"])
        print("Process           :", anomaly["process"])
        print("Current connections:",
              anomaly["current_connections"])
        print("Normal maximum    :", anomaly["normal_maximum"])
        print("Rule              :", anomaly["rule"])
        print("Severity          :", anomaly["severity"])


input("\nPress Enter to exit...")