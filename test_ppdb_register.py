import requests
import json

# Test PPDB registration endpoint
url = "http://localhost:8000/api/ppdb/register"

payload = {
    "nisn": "1234567890",
    "full_name": "Test Student Fauzi",
    "place_of_birth": "Kuningan",
    "date_of_birth": "2008-05-15",
    "gender": "Laki-laki",
    "religion": "Islam",
    "school_origin": "SMPN 1 Kuningan",
    "email": "fauziiii7888@gmail.com",
    "phone": "081234567890",
    "address": "Jl. Test No. 123",
    "father_name": "Bapak Test",
    "father_job": "Wiraswasta",
    "mother_name": "Ibu Test",
    "mother_job": "Ibu Rumah Tangga",
    "parent_phone": "081234567891",
    "parent_income": "Rp 3.000.000 - Rp 5.000.000",
    "parent_address": "Jl. Test No. 123",
    "major_choice": "Teknik Komputer dan Jaringan",
    "graduation_year": 2025,
    "average_score": "85"
}

print("="*60)
print("TESTING PPDB REGISTRATION ENDPOINT")
print("="*60)
print(f"\nURL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, json=payload)
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n🎉 REGISTRATION SUCCESSFUL!")
        print("✅ Data tersimpan ke database")
        print("✅ Email notification akan terkirim")
    else:
        print(f"\n❌ REGISTRATION FAILED!")
        print(f"Error: {response.json()}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
print("\n" + "="*60)
