import socket
from concurrent.futures import ThreadPoolExecutor

def scan_target(ip, port_range):
    open_ports = []
    for port in port_range:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = socket.getservbyport(port)
            open_ports.append((port, service))
        sock.close()
    return open_ports

def show_result(ip, port_info):
    print(f"Scanning {ip}...")
    if port_info:
        print(f"Open Ports on {ip}:")
        for port, service in port_info:
            print(f"Port {port} : Service {service}")
    else:
        print(f"No open ports found on {ip}.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    port_range = range(start_port, end_port+1)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(scan_target, target_ip, port_range): target_ip}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                port_data = future.result()
            except Exception as exc:
                print(f"{ip} generated an exception: {exc}")
            else:
                show_result(ip, port_data)
