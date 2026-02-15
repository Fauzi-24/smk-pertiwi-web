import sys
import os

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app import models
from sqlalchemy import desc

def check_data():
    db = SessionLocal()
    try:
        # Get latest 5 registrations
        registrations = db.query(models.PPDBRegistration).order_by(desc(models.PPDBRegistration.created_at)).limit(5).all()
        
        print(f"Total Registrations: {db.query(models.PPDBRegistration).count()}")
        print("-" * 50)
        if not registrations:
            print("NO DATA FOUND!")
        
        for reg in registrations:
            print(f"ID: {reg.id}")
            print(f"Created: {reg.created_at}")
            print(f"Name: {reg.full_name}")
            print(f"NISN: {reg.nisn}")
            print(f"Status: {reg.status}")
            print("-" * 50)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_data()
