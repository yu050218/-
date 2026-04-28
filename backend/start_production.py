#!/usr/bin/env python
"""
使用 Waitress WSGI 服务器启动应用
"""
import os
import sys

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
from app import app

if __name__ == '__main__':
    print("Starting Word Assessment Tool with Waitress...")
    print("Listening on 0.0.0.0:8080")
    print("Access at: http://192.168.1.110:8080")
    serve(app, host='0.0.0.0', port=80, threads=4)
