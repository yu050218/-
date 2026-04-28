#!/usr/bin/env python
"""
UPnP 端口映射工具 - 自动配置路由器端口转发
"""
import miniupnpc
import socket
import sys

def get_local_ip():
    """获取本地局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("获取本地IP失败:", e)
        return "192.168.1.110"

def setup_port_forwarding(port, description):
    """设置 UPnP 端口转发"""
    upnp = miniupnpc.UPnP()
    
    try:
        print("正在搜索 UPnP 设备...")
        upnp.discoverdelay = 200
        n = upnp.discover()
        print("发现", n, "个 UPnP 设备")
        
        if n == 0:
            print("未发现 UPnP 设备，请手动配置路由器")
            return False
        
        upnp.selectigd()
        
        external_ip = upnp.externalipaddress()
        print("外部 IP:", external_ip)
        
        local_ip = get_local_ip()
        print("本地 IP:", local_ip)
        print("正在添加端口映射:", port, "->", local_ip, ":", port)
        
        result = upnp.addportmapping(
            port, 
            "TCP", 
            local_ip, 
            port, 
            description, 
            ""
        )
        
        if result:
            print("端口映射添加成功!")
            print("访问地址: http://", local_ip, ":", port, sep="")
            return True
        else:
            print("端口映射添加失败")
            return False
            
    except Exception as e:
        print("UPnP 配置失败:", e)
        return False

def main():
    print("=== UPnP 端口映射工具 ===")
    
    port = 8080
    description = "WordAssessmentTool"
    
    success = setup_port_forwarding(port, description)
    
    if not success:
        print()
        print("请手动配置路由器端口转发:")
        print("  外部端口:", port)
        print("  内部端口:", port)
        print("  内部 IP:", get_local_ip())
        print("  协议: TCP")

if __name__ == "__main__":
    main()
