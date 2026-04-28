import requests
import socket

# 检查端口是否开放
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✓ Port {port} is open on {host}")
            return True
        else:
            print(f"✗ Port {port} is closed on {host}")
            return False
    except Exception as e:
        print(f"✗ Error checking port: {e}")
        return False
    finally:
        sock.close()

# 测试网络连接
print("Testing network connectivity...")
host = 'localhost'
port = 8000

# 检查端口
if check_port(host, port):
    # 测试请求
    url = f'http://{host}:{port}/api/register'
    data = {'username': 'testuser3', 'email': 'test3@example.com', 'password': 'password123'}
    
    print(f"\nSending request to: {url}")
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"✓ Request sent successfully")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        import traceback
        traceback.print_exc()
