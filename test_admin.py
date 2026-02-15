import requests
import os
import json

BASE_URL = "http://localhost:8000"
ADMIN_KEY = "prismoji" # From .env I saw earlier

def test_admin_login():
    print(f"\nTesting Admin Login...")
    
    # Test valid key
    try:
        response = requests.post(f"{BASE_URL}/api/admin/login", json={"admin_key": ADMIN_KEY})
        if response.status_code == 200 and response.json().get("success"):
            print("✅ Admin Login Passed")
            return response.json().get("token")
        else:
            print(f"❌ Admin Login Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Admin Login Error: {e}")
        return None

def test_admin_ppdb(token):
    print(f"\nTesting Admin PPDB Access...")
    print(f"Using token: '{token}'")
    try:
        response = requests.get(f"{BASE_URL}/api/admin/ppdb", params={"token": token})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Admin PPDB Passed: Retrieved {len(data)} records")
            if len(data) > 0:
                print(f"   Sample: {data[0]['full_name']} ({data[0]['nisn']})")
            return True
        else:
            print(f"❌ Admin PPDB Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Admin PPDB Error: {e}")
        return False

if __name__ == "__main__":
    token = test_admin_login()
    if token:
        test_admin_ppdb(token)
