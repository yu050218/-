import requests
import json

url = 'http://localhost:8000/api/register'
data = {
    'username': 'testuser2',
    'email': 'test2@example.com',
    'password': 'password123'
}

try:
    print(f"Sending request to: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    print(f"\nStatus code: {response.status_code}")
    print(f"Response headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print(f"\nResponse body: {response.text}")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
