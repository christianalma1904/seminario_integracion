import requests
import json

# Test de la URL
url = "http://127.0.0.1:8000/api/basics/area-triangulo/"
data = {
    "base": 10,
    "altura": 5
}

headers = {
    'Content-Type': 'application/json'
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")