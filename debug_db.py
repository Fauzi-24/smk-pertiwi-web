from app.database import SessionLocal
from app.models import PPDBRegistration

db = SessionLocal()
try:
    registrations = db.query(PPDBRegistration).all()
    print(f"Count: {len(registrations)}")
    for reg in registrations:
        print(f"ID: {reg.id}")
        print(f"NISN: {reg.nisn}")
        print(f"Status: {reg.status} (Type: {type(reg.status)})")
        print(f"Created At: {reg.created_at} (Type: {type(reg.created_at)})")
        print(f"Average Score: {reg.average_score} (Type: {type(reg.average_score)})")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
