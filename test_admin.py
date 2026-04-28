import requests

# 管理员登录
login_url = 'http://localhost:8000/api/login'
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    print("测试管理员登录...")
    response = requests.post(login_url, json=login_data)
    print(f"登录状态码: {response.status_code}")
    result = response.json()
    print(f"登录响应: {result}")
    
    if response.status_code == 200 and 'token' in result:
        token = result['token']
        print(f"\n管理员Token获取成功: {token[:20]}...")
        
        # 测试获取用户列表
        print("\n测试获取用户列表...")
        headers = {'Authorization': f'Bearer {token}'}
        users_response = requests.get('http://localhost:8000/api/admin/users', headers=headers)
        print(f"获取用户列表状态码: {users_response.status_code}")
        if users_response.status_code == 200:
            users = users_response.json()
            print(f"用户列表 ({len(users)} 个用户):")
            for user in users[:5]:  # 只显示前5个
                print(f"  - ID: {user['id']}, 用户名: {user['username']}, 邮箱: {user['email']}")
        
        # 测试获取词库
        print("\n测试获取词库...")
        wordbank_response = requests.get('http://localhost:8000/api/admin/word-bank', headers=headers)
        print(f"获取词库状态码: {wordbank_response.status_code}")
        if wordbank_response.status_code == 200:
            words = wordbank_response.json()
            print(f"词库单词数量: {len(words)}")
            
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()