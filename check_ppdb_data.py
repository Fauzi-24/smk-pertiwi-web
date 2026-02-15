from app.database import SessionLocal
from app import models
from sqlalchemy import desc

db = SessionLocal()
try:
    # Get latest 5 registrations
    registrations = db.query(models.PPDBRegistration).order_by(desc(models.PPDBRegistration.created_at)).limit(5).all()
    
    print(f"Total Registrations: {db.query(models.PPDBRegistration).count()}")
    print("-" * 50)
    for reg in registrations:
        print(f"ID: {reg.id}")
        print(f"Created: {reg.created_at}")
        print(f"Name: {reg.full_name}")
        print(f"NISN: {reg.nisn}")
        print(f"Status: {reg.status}")
        print("-" * 50)
finally:
    db.close()
