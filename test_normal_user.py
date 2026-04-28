#!/usr/bin/env python
"""
测试普通用户访问单词卡片功能
"""
import requests
import json

def test_normal_user():
    base_url = "http://127.0.0.1"
    
    print("=== 创建测试用户 ===")
    try:
        # 先尝试注册一个新用户
        register_data = {
            "username": "normaluser",
            "email": "normal@test.com",
            "password": "test123456"
        }
        response = requests.post(f"{base_url}/api/register", json=register_data)
        print(f"注册状态码: {response.status_code}")
        
        # 登录
        print("\n=== 测试普通用户登录 ===")
        login_data = {
            "username": "normaluser",
            "password": "test123456"
        }
        response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            user_id = data.get('user_id')
            is_admin = data.get('is_admin')
            
            print(f"用户ID: {user_id}")
            print(f"是否管理员: {is_admin}")
            print(f"Token: {token[:20]}...")
            
            # 测试访问单词 API
            print("\n=== 测试普通用户访问单词 API ===")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/api/words", headers=headers)
            print(f"API 状态码: {response.status_code}")
            
            if response.status_code == 200:
                words = response.json()
                print(f"✓ 成功获取 {len(words)} 个单词")
                print(f"第一个单词: {words[0]['word']} - {words[0]['meaning']}")
            else:
                print(f"✗ 访问失败: {response.json()}")
            
            # 测试访问管理员 API (应该失败)
            print("\n=== 测试普通用户访问管理员 API ===")
            response = requests.get(f"{base_url}/api/admin/word-bank", headers=headers)
            print(f"管理员 API 状态码: {response.status_code}")
            if response.status_code == 403:
                print("✓ 普通用户无法访问管理员 API (正确)")
            else:
                print(f"✗ 意外结果: {response.json()}")
                
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_normal_user()
