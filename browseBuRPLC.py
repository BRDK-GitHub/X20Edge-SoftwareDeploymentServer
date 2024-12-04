import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((str(ip), port))
        sock.close()

        if result == 0:
            return ip
        return None
    except Exception as e:
        print(f"Error scanning {ip}: {e}")
        return None

def scan_subnet(subnet, port, max_workers=20):
    network = ipaddress.ip_network(subnet, strict=False)
    open_ips = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_port, ip, port) for ip in network.hosts()]

        for future in as_completed(futures):
            ip = future.result()
            if ip:
                open_ips.append(str(ip))

    return open_ips

if __name__ == "__main__":
    # Example usage:
    subnet = '192.168.30.0/24'
    port = 11169 # ANSL port
    open_ips = scan_subnet(subnet, port, max_workers=20)

    print("\nB&R PLCs found at the following IPs:")
    for ip in open_ips:
        print(ip)
