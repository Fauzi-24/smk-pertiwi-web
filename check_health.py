import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Backend is reachable.")
    else:
        print("Backend returned non-200 status.")
except Exception as e:
    print(f"Failed to connect: {e}")
