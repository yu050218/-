import requests

# 测试不同的URL
urls = [
    'http://localhost:8000/api/register',
    'http://localhost:8000/api/login',
    'http://localhost:8000/api/test/start'
]

data = {'username': 'test', 'email': 'test@test.com', 'password': 'pass'}

for url in urls:
    print(f"\nTesting: {url}")
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
