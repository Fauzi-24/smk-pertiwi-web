import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print(f"Testing Health Check at {BASE_URL}/health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health Check Passed:", response.json())
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health Check Connection Error: {e}")
        return False

def test_chat():
    print(f"\nTesting Chat API at {BASE_URL}/api/chat...")
    payload = {
        "message": "Halo, siapa kamu?",
        "history": [],
        "session_id": "test-session"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Chat API Passed:", data.get("message")[:50] + "...")
                return True
            else:
                print("❌ Chat API Returned Success=False:", data)
                return False
        else:
            print(f"❌ Chat API Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat API Connection Error: {e}")
        return False

def test_ppdb():
    print(f"\nTesting PPDB Registration at {BASE_URL}/api/ppdb/register...")
    # Generate unique NISN to avoid conflict
    nisn = f"TEST{int(time.time())}"
    payload = {
        "nisn": nisn,
        "full_name": "Test Siswa",
        "place_of_birth": "Jakarta",
        "date_of_birth": "2008-01-01",
        "gender": "Laki-laki",
        "religion": "Islam",
        "school_origin": "SMP Tes",
        "email": "test@example.com",
        "phone": "081234567890",
        "address": "Jl. Tes No. 1",
        "father_name": "Ayah Tes",
        "father_job": "Wiraswasta",
        "mother_name": "Ibu Tes",
        "mother_job": "Ibu Rumah Tangga",
        "parent_phone": "081234567891",
        "parent_income": "5000000",
        "parent_address": "Jl. Tes No. 1",
        "major_choice": "RPL",
        "graduation_year": 2024,
        "average_score": "85.5",
        "status": "pending"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ppdb/register", json=payload)
        if response.status_code == 200:
            print("✅ PPDB Registration Passed:", response.json())
            return True
        else:
            print(f"❌ PPDB Registration Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ PPDB Connection Error: {e}")
        return False

if __name__ == "__main__":
    health = test_health()
    if health:
        test_chat()
        test_ppdb()
    else:
        print("Skipping other tests due to health check failure.")
