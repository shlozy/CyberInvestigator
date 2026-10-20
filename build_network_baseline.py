import psutil
import json
import time
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("              NETWORK DESTINATION BASELINE")
print("=" * 75)

print("\nWe will collect 5 normal observations.")
print("Keep your computer in normal use during collection.\n")

observations = []

for sample_number in range(1, 6):

    print(f"Collecting observation {sample_number}/5...")

    connections = psutil.net_connections(kind="inet")

    observation = {}

    for connection in connections:

        if connection.status != "ESTABLISHED":
            continue

        if not connection.raddr:
            continue

        # Find process name
        process_name = "Unknown"

        if connection.pid:
            try:
                process = psutil.Process(connection.pid)
                process_name = process.name()

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"

        remote_ip = connection.raddr.ip
        remote_port = connection.raddr.port

        if process_name not in observation:
            observation[process_name] = []

        destination = {
            "ip": remote_ip,
            "port": remote_port
        }

        if destination not in observation[process_name]:
            observation[process_name].append(destination)

    observations.append(observation)

    print(observation)

    if sample_number < 5:
        time.sleep(5)


# --------------------------------------------------
# COMBINE ALL OBSERVATIONS
# --------------------------------------------------

network_baseline = {}

for observation in observations:

    for process, destinations in observation.items():

        if process not in network_baseline:
            network_baseline[process] = []

        for destination in destinations:

            if destination not in network_baseline[process]:
                network_baseline[process].append(destination)


# --------------------------------------------------
# SAVE BASELINE
# --------------------------------------------------

baseline_data = {
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "samples": len(observations),
    "network_baseline": network_baseline
}


with open("network_baseline.json", "w") as file:
    json.dump(baseline_data, file, indent=4)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 75)
print("              NETWORK BASELINE CREATED")
print("=" * 75)

for process, destinations in network_baseline.items():

    print(f"\n{process}")

    for destination in destinations:

        print(
            f"  {destination['ip']} : "
            f"{destination['port']}"
        )


print("\nNetwork baseline saved to: network_baseline.json")

input("\nPress Enter to exit...")