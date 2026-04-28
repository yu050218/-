import socket
import time

def test_connection():
    host = "192.168.1.110"
    port = 8000

    print(f"Testing connection to {host}:{port}")
    print(f"Local hostname: {socket.gethostname()}")
    print(f"Local IPs: {socket.gethostbyname_ex(socket.gethostname())[2]}")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        print(f"Connecting to {host}:{port}...")

        # Try to connect
        result = sock.connect_ex((host, port))
        print(f"connect_ex result: {result}")

        if result == 0:
            print("Connection successful!")

            # Try to send HTTP request
            request = b"GET / HTTP/1.1\r\nHost: 192.168.1.110\r\n\r\n"
            sock.sendall(request)
            print("Sent HTTP request")

            # Receive response
            response = sock.recv(4096)
            print(f"Received response: {response[:200]}")
            sock.close()
            return True
        else:
            print(f"Connection failed with error code: {result}")
            sock.close()
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

def check_all_interfaces():
    print("\n=== Checking all network interfaces ===")
    try:
        hostname = socket.gethostname()
        ip_list = socket.gethostbyname_ex(hostname)[2]
        for ip in ip_list:
            print(f"  Interface: {ip}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.bind((ip, 0))
                print(f"    -> Can bind: YES")
            except Exception as e:
                print(f"    -> Can bind: NO ({e})")
            sock.close()
    except Exception as e:
        print(f"Error checking interfaces: {e}")

if __name__ == "__main__":
    test_connection()
    check_all_interfaces()
