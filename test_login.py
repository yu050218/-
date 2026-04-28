import requests

url = 'http://localhost:8000/api/login'
data = {
    'username': 'testuser2',
    'password': 'password123'
}

try:
    response = requests.post(url, json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")