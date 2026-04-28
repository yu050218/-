#!/usr/bin/env python
"""
局域网访问修复工具
"""
import os
import subprocess
import sys

def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    print("=== 局域网访问修复工具 ===")
    print("正在检查网络配置...")
    
    # 检查端口监听
    print("\n1. 检查端口监听状态:")
    stdout, stderr, code = run_command("netstat -ano | findstr :8080")
    print(stdout)
    if code != 0:
        print(f"错误: {stderr}")
    
    # 检查防火墙规则
    print("\n2. 检查防火墙规则:")
    stdout, stderr, code = run_command('netsh advfirewall firewall show rule name="Allow All HTTP Ports"')
    if "规则名称" in stdout:
        print("防火墙规则已存在")
    else:
        print("防火墙规则不存在，需要手动添加")
    
    # 测试本地连接
    print("\n3. 测试本地连接:")
    stdout, stderr, code = run_command("curl -s http://192.168.1.110:8080/ -o /dev/null -w 'HTTP Status: %{http_code}\n'")
    print(stdout)
    
    print("\n=== 修复建议 ===")
    print("1. 确保路由器关闭了 AP 隔离/客户端隔离功能")
    print("2. 确保手机和服务器连接在同一个 WiFi 网络")
    print("3. 在路由器中添加端口转发规则: 8080 -> 192.168.1.110:8080")
    print("4. 尝试使用手机浏览器访问: http://192.168.1.110:8080")

if __name__ == "__main__":
    main()
