import psutil
import json
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("              NETWORK DESTINATION DETECTOR")
print("=" * 75)


# --------------------------------------------------
# LOAD BASELINE
# --------------------------------------------------

with open("network_baseline.json", "r") as file:
    baseline_data = json.load(file)

network_baseline = baseline_data["network_baseline"]

print("\nNetwork baseline loaded successfully.")
print("Baseline created at:", baseline_data["created_at"])


# --------------------------------------------------
# COLLECT CURRENT CONNECTIONS
# --------------------------------------------------

print("\nCollecting current network activity...\n")

connections = psutil.net_connections(kind="inet")

current_connections = []


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

    remote_ip = connection.raddr.ip
    remote_port = connection.raddr.port

    current_connection = {
        "process": process_name,
        "ip": remote_ip,
        "port": remote_port
    }

    current_connections.append(current_connection)


# --------------------------------------------------
# DETECT NEW DESTINATIONS
# --------------------------------------------------

new_destinations = []


for connection in current_connections:

    process = connection["process"]
    ip = connection["ip"]
    port = connection["port"]

    known_destinations = network_baseline.get(process, [])

    destination_known = False

    for destination in known_destinations:

        if (
            destination["ip"] == ip
            and
            destination["port"] == port
        ):
            destination_known = True
            break

    if not destination_known:

        new_destination = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "process": process,
            "ip": ip,
            "port": port,
            "rule": "New process-to-destination relationship",
            "severity": "LOW"
        }

        new_destinations.append(new_destination)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("=" * 75)
print("                    DETECTION RESULTS")
print("=" * 75)

print("\nCurrent established connections:", len(current_connections))

print("\nNew destinations detected:", len(new_destinations))


if len(new_destinations) == 0:

    print("\nNo new process-to-destination relationships detected.")

else:

    for alert in new_destinations:

        print("\n⚠️ NEW DESTINATION")

        print("Time       :", alert["time"])
        print("Process    :", alert["process"])
        print("Remote IP  :", alert["ip"])
        print("Remote Port:", alert["port"])
        print("Rule       :", alert["rule"])
        print("Severity   :", alert["severity"])

        print("Note       : This is an investigation signal,")
        print("             not proof of malicious activity.")


input("\nPress Enter to exit...")