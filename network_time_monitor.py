
import psutil
import time
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 TIME-BASED MONITOR")
print("=" * 75)

SAMPLES = 6
INTERVAL = 5

previous_counts = {}

print(f"\nTaking {SAMPLES} observations, {INTERVAL} seconds apart.")
print("Use your computer normally during collection.\n")

for sample in range(1, SAMPLES + 1):

    current_counts = {}

    connections = psutil.net_connections(kind="inet")

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

        current_counts[process_name] = (
            current_counts.get(process_name, 0) + 1
        )

    timestamp = datetime.now().strftime("%H:%M:%S")

    print("-" * 75)
    print(f"Observation {sample}/{SAMPLES} | Time: {timestamp}")

    if not current_counts:
        print("No established external connections found.")

    for process, count in sorted(current_counts.items()):

        if process in previous_counts:
            change = count - previous_counts[process]

            if change > 0:
                change_text = f"+{change}"
            else:
                change_text = str(change)

            print(
                f"{process}: {count} connections "
                f"(change: {change_text})"
            )

        else:
            print(
                f"{process}: {count} connections "
                "(first observation or newly observed process)"
            )

    previous_counts = current_counts.copy()

    if sample < SAMPLES:
        time.sleep(INTERVAL)

print("\nMonitoring experiment complete.")

input("\nPress Enter to exit...")