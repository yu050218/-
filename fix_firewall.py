#!/usr/bin/env python
"""
Windows 防火墙配置工具 - 修复局域网访问问题
"""
import os
import subprocess
import sys

def run_as_admin():
    """检查是否以管理员权限运行"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_cmd(cmd, show_output=True):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        if show_output and output.strip():
            print(output)
        return result.returncode == 0
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def main():
    print("=" * 60)
    print("Windows 防火墙配置工具")
    print("=" * 60)

    if not run_as_admin():
        print("\n错误: 需要管理员权限运行此脚本!")
        print("请右键选择 '以管理员身份运行' Python")
        input("\n按回车键退出...")
        return

    print("\n正在配置防火墙...")

    # 1. 添加端口 80 入站规则
    print("\n[1] 添加端口 80 入站规则...")
    rules = [
        'netsh advfirewall firewall add rule name="HTTP Port 80" dir=in action=allow protocol=TCP localport=80',
        'netsh advfirewall firewall add rule name="HTTP Port 80 LAN" dir=in action=allow protocol=TCP localport=80 remoteip=192.168.0.0/16',
        'netsh advfirewall firewall add rule name="HTTP Port 80 LAN2" dir=in action=allow protocol=TCP localport=80 remoteip=192.168.1.0/24',
    ]

    for rule in rules:
        print(f"  执行: {rule}")
        run_cmd(rule)

    # 2. 关闭特定文件的防火墙（可选，用于调试）
    print("\n[2] 检查当前防火墙策略...")
    run_cmd('netsh advfirewall show allprofiles | findstr "防火墙策略"')

    # 3. 显示所有入站规则
    print("\n[3] 当前 HTTP 相关规则:")
    run_cmd('netsh advfirewall firewall show rule name="HTTP Port 80"')
    run_cmd('netsh advfirewall firewall show rule name="HTTP Port 80 LAN"')

    # 4. 测试服务器连接
    print("\n[4] 测试服务器连接...")
    run_cmd('curl -s http://127.0.0.1/ > nul && echo 本地连接: 成功 || echo 本地连接: 失败')

    print("\n" + "=" * 60)
    print("配置完成!")
    print("=" * 60)
    print("""
请尝试从其他设备访问: http://192.168.1.110

如果仍有问题，请尝试:
1. 关闭 Windows Defender 防火墙（临时测试）
2. 禁用其他安全软件（如 360、腾讯电脑管家等）
3. 检查是否有其他防火墙规则阻止连接
    """)

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
