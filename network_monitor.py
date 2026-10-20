import psutil
from datetime import datetime

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 NETWORK MONITOR + DETECTION")
print("=" * 75)

print("\nCollecting network events...\n")

connections = psutil.net_connections(kind="inet")

events = []

for connection in connections:

    process_name = "Unknown"

    if connection.pid:
        try:
            process = psutil.Process(connection.pid)
            process_name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"

    if connection.laddr:
        local_ip = connection.laddr.ip
        local_port = connection.laddr.port
    else:
        local_ip = "-"
        local_port = "-"

    if connection.raddr:
        remote_ip = connection.raddr.ip
        remote_port = connection.raddr.port
    else:
        remote_ip = "-"
        remote_port = "-"

    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "process": process_name,
        "pid": connection.pid,
        "local_ip": local_ip,
        "local_port": local_port,
        "remote_ip": remote_ip,
        "remote_port": remote_port,
        "status": connection.status
    }

    events.append(event)


# ---------------------------------------------------------
# DETECTION RULE
# ---------------------------------------------------------

process_connections = {}

for event in events:

    if event["status"] == "ESTABLISHED" and event["remote_ip"] != "-":

        process_name = event["process"]

        if process_name not in process_connections:
            process_connections[process_name] = 0

        process_connections[process_name] += 1


alerts = []

for process_name, count in process_connections.items():

    if count >= 5:

        alert = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "process": process_name,
            "connection_count": count,
            "rule": "Repeated external connections",
            "severity": "LOW"
        }

        alerts.append(alert)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("Events collected:", len(events))

print("\n" + "=" * 75)
print("                    DETECTION RESULTS")
print("=" * 75)

print("\nProcesses with ESTABLISHED external connections:")

for process_name, count in process_connections.items():

    print(f"{process_name}: {count}")


print("\n" + "=" * 75)
print("                         ALERTS")
print("=" * 75)

if len(alerts) == 0:

    print("\nNo detection rules were triggered.")

else:

    for alert in alerts:

        print("\n🚨 ALERT")
        print("Time             :", alert["time"])
        print("Process          :", alert["process"])
        print("Connections      :", alert["connection_count"])
        print("Rule             :", alert["rule"])
        print("Severity         :", alert["severity"])


input("\nPress Enter to exit...")