#!/usr/bin/env python
"""
测试单词卡片 API 是否正常工作
"""
import requests
import json

def main():
    base_url = "http://127.0.0.1"
    
    # 1. 测试登录
    print("=== 测试登录 ===")
    login_data = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"获取到 token: {token[:20]}...")
            
            # 2. 使用 token 访问单词 API
            print("\n=== 测试访问单词 API ===")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/api/words", headers=headers)
            print(f"API 状态码: {response.status_code}")
            
            if response.status_code == 200:
                words = response.json()
                print(f"获取到 {len(words)} 个单词")
                if words:
                    print(f"第一个单词: {words[0]}")
            else:
                print(f"API 错误: {response.json()}")
        else:
            print(f"登录失败: {response.json()}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    main()
