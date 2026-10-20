import psutil

print("=" * 75)
print("                    CYBER INVESTIGATOR")
print("                 NETWORK BEHAVIOR ANALYSIS")
print("=" * 75)

print("\nAnalyzing current network activity...\n")

connections = psutil.net_connections(kind="inet")

process_data = {}


# --------------------------------------------------
# COLLECT INFORMATION
# --------------------------------------------------

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


    # Remote information
    remote_ip = connection.raddr.ip
    remote_port = connection.raddr.port


    # Create process entry if it doesn't exist
    if process_name not in process_data:

        process_data[process_name] = {
            "total_connections": 0,
            "remote_ips": set(),
            "remote_ports": set()
        }


    # Add information
    process_data[process_name]["total_connections"] += 1

    process_data[process_name]["remote_ips"].add(remote_ip)

    process_data[process_name]["remote_ports"].add(remote_port)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("=" * 75)
print("                    NETWORK ANALYSIS")
print("=" * 75)

for process, data in process_data.items():

    print("\nProcess:", process)

    print(
        "Total connections:",
        data["total_connections"]
    )

    print(
        "Unique remote IPs:",
        len(data["remote_ips"])
    )

    print(
        "Remote ports:",
        sorted(data["remote_ports"])
    )


input("\nPress Enter to exit...")