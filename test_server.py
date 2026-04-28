#!/usr/bin/env python
"""
简单的测试服务器，用于验证局域网连接
"""
import socket
import threading
import time

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            print(f"[RECEIVED] {addr}: {data[:100]}")
        
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Test Server</h1><p>Connection successful!</p></body></html>"
        conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start_test_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"[LISTENING] Test server on 0.0.0.0:{port}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except Exception as e:
        print(f"[FAILED TO START] {e}")
        server.close()

if __name__ == "__main__":
    start_test_server(5000)
