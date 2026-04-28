#!/usr/bin/env python
"""
完整的网络诊断和服务器测试
"""
import socket
import subprocess
import sys
import time

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def get_local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
    except:
        pass
    return ips

def test_port_connectivity(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def main():
    print("=" * 60)
    print("网络诊断报告")
    print("=" * 60)

    # 1. 服务器状态
    print("\n[1] 服务器端口状态:")
    output = run_cmd('netstat -ano | findstr ":80 " | findstr "LISTEN"')
    print(output if output.strip() else "没有发现端口 80 在监听")

    # 2. 本地 IP
    print("\n[2] 本机 IP 地址:")
    ips = get_local_ips()
    for ip in ips:
        print(f"  - {ip}")

    # 3. 测试连接
    print("\n[3] 测试本地连接 (127.0.0.1:80):")
    if test_port_connectivity("127.0.0.1", 80):
        print("  结果: 成功连接")
    else:
        print("  结果: 连接失败")

    print("\n[4] 测试局域网连接 (192.168.1.110:80):")
    if test_port_connectivity("192.168.1.110", 80):
        print("  结果: 成功连接")
    else:
        print("  结果: 连接失败")

    # 4. 防火墙状态
    print("\n[5] 防火墙规则检查:")
    output = run_cmd('netsh advfirewall firewall show rule name="Allow Port 8000 HTTP"')
    if "不存在" in output or not output.strip():
        print("  'Allow Port 8000 HTTP' 规则不存在")
    else:
        print("  'Allow Port 8000 HTTP' 规则存在")

    # 5. 建议
    print("\n" + "=" * 60)
    print("可能的问题和解决方案:")
    print("=" * 60)
    print("""
1. 如果本地连接成功但局域网失败:
   - 检查路由器是否开启了 AP 隔离/客户端隔离
   - 登录路由器管理页面 (通常是 192.168.1.1)

2. 如果手机显示"服务器无响应":
   - 确保服务器电脑和手机在同一 WiFi 网络
   - 尝试重启路由器
   - 尝试重启手机 WiFi

3. 临时解决方案 - 使用 ngrok 内网穿透:
   - 安装 ngrok: https://ngrok.com/download
   - 运行: ngrok http 80
   - 使用生成的公网地址访问
    """)

if __name__ == "__main__":
    main()
