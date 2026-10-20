import psutil
import json
from datetime import datetime


print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                  BASELINE COLLECTION")
print("=" * 75)

print("\nCollecting current network activity...\n")


connections = psutil.net_connections(kind="inet")

process_connections = {}


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


    if process_name not in process_connections:
        process_connections[process_name] = 0

    process_connections[process_name] += 1


baseline = {
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "process_connections": process_connections
}


with open("baseline.json", "w") as file:
    json.dump(baseline, file, indent=4)


print("Baseline created successfully!\n")

print("=" * 75)
print("CURRENT BASELINE")
print("=" * 75)

for process, count in process_connections.items():
    print(f"{process}: {count}")

print("\nBaseline saved to: baseline.json")

input("\nPress Enter to exit...")