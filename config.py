#config.py

import socket
import grpc

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

ips = ["10.10.152.85","10.10.152.85","10.10.159.255"] #gulnars, gandab window, ...,alicia's linux
print(f"Hostname: {hostname}")
nicknames = ["Tail","Body","Head"]


def get_node_id():
    # Get the server's IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Use the last octet of the IP address as the node ID
    node_id = int(ip_address.split(".")[-1])
    return node_id

def ip(address):
    if address == nodes_addresses[0]:
        return ips[0]
    elif address == nodes_addresses[1]:
        return ips[1]
    else:
        return ips[2]

time_limit = 60
total_processes = 3

first_port = 50051
last_port = first_port + total_processes -1
nodes_addresses = [first_port + i for i in range(total_processes)]

# Increase the maximum metadata size
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB
]
