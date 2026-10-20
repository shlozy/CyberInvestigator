import subprocess

print("=" * 70)
print("              CYBER INVESTIGATOR")
print("             NETWORK PROTOCOL VIEW")
print("=" * 70)

print("\nReading active network connections...\n")

result = subprocess.run(
    ["netstat", "-ano"],
    capture_output=True,
    text=True
)

lines = result.stdout.splitlines()

tcp_count = 0
udp_count = 0

for line in lines:
    line = line.strip()

    if line.startswith("TCP"):
        parts = line.split()

        if len(parts) >= 4:
            protocol = parts[0]
            local_address = parts[1]
            remote_address = parts[2]
            state = parts[3]

            tcp_count += 1

            print("-" * 70)
            print("Protocol        :", protocol)
            print("Local Address   :", local_address)
            print("Remote Address  :", remote_address)
            print("State           :", state)

    elif line.startswith("UDP"):
        parts = line.split()

        if len(parts) >= 3:
            protocol = parts[0]
            local_address = parts[1]
            remote_address = parts[2]

            udp_count += 1

            print("-" * 70)
            print("Protocol        :", protocol)
            print("Local Address   :", local_address)
            print("Remote Address  :", remote_address)
            print("State           : Not applicable")


print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("TCP entries found :", tcp_count)
print("UDP entries found :", udp_count)

input("\nPress Enter to exit...")