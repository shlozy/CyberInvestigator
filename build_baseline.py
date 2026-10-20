import psutil
import json
import time
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                MULTI-SAMPLE BASELINE")
print("=" * 75)

print("\nWe will collect 5 observations.")
print("Keep your computer in normal use during collection.\n")

observations = []

for sample_number in range(1, 6):

    print(f"Collecting observation {sample_number}/5...")

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

    observations.append(process_connections)

    print(process_connections)

    if sample_number < 5:
        time.sleep(5)


all_processes = set()

for observation in observations:
    all_processes.update(observation.keys())


baseline = {}

for process in all_processes:

    values = []

    for observation in observations:
        values.append(observation.get(process, 0))

    baseline[process] = {
        "minimum": min(values),
        "maximum": max(values),
        "average": round(sum(values) / len(values), 2)
    }


baseline_data = {
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "samples": len(observations),
    "process_baseline": baseline
}


with open("baseline.json", "w") as file:
    json.dump(baseline_data, file, indent=4)


print("\n" + "=" * 75)
print("                    BASELINE CREATED")
print("=" * 75)

for process, values in baseline.items():

    print(
        f"{process}: "
        f"min={values['minimum']}, "
        f"max={values['maximum']}, "
        f"average={values['average']}"
    )

print("\nBaseline saved to: baseline.json")

input("\nPress Enter to exit...")