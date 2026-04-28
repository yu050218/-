import socket
import sys

def test_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.110"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    print(f"Testing connectivity to {host}:{port}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"IP addresses: {socket.gethostbyname_ex(socket.gethostname())[2]}")

    if test_port(host, port):
        print(f"SUCCESS: Port {port} is reachable on {host}")
    else:
        print(f"FAILED: Port {port} is NOT reachable on {host}")
