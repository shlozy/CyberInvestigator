import psutil
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                CONNECTION FREQUENCY")
print("=" * 75)

print("\nCollecting current network activity...\n")

connections = psutil.net_connections(kind="inet")

process_connections = {}


# --------------------------------------------------
# COUNT CONNECTIONS FOR EACH PROCESS
# --------------------------------------------------

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


# --------------------------------------------------
# DETECTION
# --------------------------------------------------

alerts = []

THRESHOLD = 10

for process, count in process_connections.items():

    if count >= THRESHOLD:

        alert = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "process": process,
            "connection_count": count,
            "rule": "High connection frequency",
            "severity": "LOW"
        }

        alerts.append(alert)


# --------------------------------------------------
# DISPLAY CURRENT ACTIVITY
# --------------------------------------------------

print("=" * 75)
print("                    CURRENT ACTIVITY")
print("=" * 75)

for process, count in process_connections.items():

    print(f"{process}: {count} established connections")


# --------------------------------------------------
# DISPLAY ALERTS
# --------------------------------------------------

print("\n" + "=" * 75)
print("                    DETECTION RESULTS")
print("=" * 75)

print("\nConnection frequency threshold:", THRESHOLD)

if len(alerts) == 0:

    print("\nNo high-frequency connection behavior detected.")

else:

    for alert in alerts:

        print("\n⚠️ HIGH CONNECTION FREQUENCY")

        print("Time       :", alert["time"])
        print("Process    :", alert["process"])
        print("Connections:", alert["connection_count"])
        print("Rule       :", alert["rule"])
        print("Severity   :", alert["severity"])

        print("\nNote: High connection frequency is an")
        print("investigation signal, not proof of malicious activity.")


input("\nPress Enter to exit...")