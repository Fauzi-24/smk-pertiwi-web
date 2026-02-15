from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
import os
import time
from datetime import datetime

from .. import models, database
from ..services import email_service
from ..config import settings

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(database.get_db),
    key: Optional[str] = None
):
    # Verify key (using settings or header if middleware handles it, 
    # but middleware + key arg is safer for direct calls)
    correct_key = settings.admin_key
    # Check if key is provided either in query (less secure) or assume middleware
    # For now, let's just proceed or check if key is in query for direct access
    if key and key != correct_key:
         raise HTTPException(status_code=401, detail="Invalid Admin Key")

    # 1. Total Registrants
    total = db.query(models.PPDBRegistration).count()
    
    # 2. Status Counts
    verified = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.status == models.PPDBStatus.VERIFIED).count()
    accepted = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.status == models.PPDBStatus.ACCEPTED).count()
    pending = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.status == models.PPDBStatus.PENDING).count()
    rejected = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.status == models.PPDBStatus.REJECTED).count()
    
    # 3. Per Major Counts
    major_stats = db.query(
        models.PPDBRegistration.jurusan_pilihan, 
        func.count(models.PPDBRegistration.id)
    ).group_by(models.PPDBRegistration.jurusan_pilihan).all()
    
    per_major = {major or "Unknown": count for major, count in major_stats}
    
    return {
        "total": total,
        "verified": verified,
        "accepted": accepted,
        "pending": pending,
        "rejected": rejected,
        "per_major": per_major
    }

# Simple Request Models
class AdminLoginRequest(BaseModel):
    admin_key: str

class AdminLoginResponse(BaseModel):
    success: bool
    token: str

# Response Model for PPDB (full data)
class PPDBResponse(BaseModel):
    id: int
    nisn: str
    full_name: str
    place_of_birth: str
    date_of_birth: str
    gender: str
    religion: str
    school_origin: str
    email: str
    phone: str
    address: str
    father_name: str
    father_job: str
    mother_name: str
    mother_job: str
    parent_phone: str
    parent_income: str
    parent_address: str
    major_choice: str
    graduation_year: int
    average_score: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

# Security: Login Rate Limiting
# IP -> { "count": int, "reset_time": float, "lockout_until": float }
login_attempts = {}

def check_login_rate_limit(ip: str):
    now = time.time()
    if ip in login_attempts:
        data = login_attempts[ip]
        # Check lockout
        if data["lockout_until"] > now:
            remaining = int((data["lockout_until"] - now) / 60) + 1
            print(f"🛑 Security: Blocked login attempt from locked IP {ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed attempts. Try again in {remaining} minutes."
            )
        # Check reset window
        if data["reset_time"] < now:
            data["count"] = 0
            data["reset_time"] = now + 900  # 15 minutes window
            data["lockout_until"] = 0

def record_login_attempt(ip: str, success: bool):
    now = time.time()
    if ip not in login_attempts:
        login_attempts[ip] = { "count": 0, "reset_time": now + 900, "lockout_until": 0 }
    
    data = login_attempts[ip]
    
    if success:
        # Reset on success
        data["count"] = 0
        data["reset_time"] = now + 900
        data["lockout_until"] = 0
    else:
        # Increment on failure
        data["count"] += 1
        print(f"⚠️ Security: Failed login attempt {data['count']}/5 from {ip}")
        if data["count"] >= 5:
            data["lockout_until"] = now + 900  # Lockout for 15 mins
            print(f"🚫 Security: IP {ip} locked out due to excessive failures")

@router.post("/login", response_model=AdminLoginResponse)
def admin_login(request: AdminLoginRequest, req: Request):
    # Get IP properly behind Vercel Proxy
    forwarded = req.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0]
    else:
        client_ip = req.client.host if req.client else "unknown"
    
    print(f"🔍 Login Attempt from IP: {client_ip}")

    # Check rate limit before validating key
    # check_login_rate_limit(client_ip) # Disabled temporarily for debugging
    
    correct_key = settings.admin_key
    
    # Debug logs (Check Vercel Function Logs if this prints)
    print(f"🔑 Received Key: {request.admin_key}")
    print(f"🔒 Expected Key: {correct_key}")
    
    if not correct_key:
        print("❌ Server Error: Admin Key not configured in settings")
        raise HTTPException(status_code=500, detail="Server configuration error: Admin Key not set")
    
    if request.admin_key == correct_key:
        record_login_attempt(client_ip, True)
        return {"success": True, "token": "admin-session-valid"}
    else:
        record_login_attempt(client_ip, False)
        print("⛔ Invalid Admin Key provided")
        raise HTTPException(status_code=401, detail=f"Invalid Admin Key. Received: {request.admin_key}")

@router.get("/ppdb")
def get_all_ppdb(token: str, db: Session = Depends(database.get_db)):
    correct_key = settings.admin_key
    if token != "admin-session-valid" and token != correct_key:
         raise HTTPException(status_code=401, detail="Unauthorized")

    submissions = db.query(models.PPDBRegistration).order_by(models.PPDBRegistration.created_at.desc()).all()
    
    # Manually convert to list of dicts to avoid serialization issues
    results = []
    for s in submissions:
        results.append({
            "id": s.id,
            "nisn": s.nisn,
            "full_name": s.full_name,
            "place_of_birth": s.place_of_birth,
            "date_of_birth": s.date_of_birth,
            "gender": s.gender,
            "religion": s.religion,
            "school_origin": s.school_origin,
            "email": s.email,
            "phone": s.phone,
            "address": s.address,
            "father_name": s.father_name,
            "father_job": s.father_job,
            "mother_name": s.mother_name,
            "mother_job": s.mother_job,
            "parent_phone": s.parent_phone,
            "parent_income": s.parent_income,
            "parent_address": s.parent_address,
            "major_choice": s.major_choice,
            "graduation_year": s.graduation_year,
            "average_score": s.average_score,
            "status": str(s.status), # Handle Enum
            "notes": s.notes,
            "created_at": s.created_at.isoformat() if s.created_at else None
        })
    return results

class UpdateStatusRequest(BaseModel):
    status: str
    token: str

@router.put("/ppdb/{id}/status")
def update_ppdb_status(id: int, request: UpdateStatusRequest, db: Session = Depends(database.get_db)):
    correct_key = settings.admin_key
    if request.token != "admin-session-valid" and request.token != correct_key:
         raise HTTPException(status_code=401, detail="Unauthorized")
    
    entry = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Data not found")
    
    valid_statuses = ["pending", "verified", "accepted", "rejected"]
    if request.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    entry.status = request.status
    db.commit()
    
    # Send email notification when status changes to accepted/rejected
    try:
        if request.status == "accepted":
            # Import asyncio to run async function
            import asyncio
            asyncio.create_task(
                email_service.send_acceptance_email(
                    student_email=entry.email,
                    student_name=entry.full_name,
                    nisn=entry.nisn,
                    major=entry.major_choice
                )
            )
            print(f"✅ Acceptance email queued for {entry.email}")
        elif request.status == "rejected":
            import asyncio
            asyncio.create_task(    
                email_service.send_rejection_email(
                    student_email=entry.email,
                    student_name=entry.full_name,
                    nisn=entry.nisn
                )
            )
            print(f"✅ Rejection email queued for {entry.email}")
    except Exception as e:
        # Log error but don't fail the status update
        print(f"⚠️ Failed to queue status email: {e}")
    
    return {"success": True, "message": f"Status updated to {request.status}"}

@router.delete("/ppdb/{id}")
def delete_ppdb(id: int, token: str, db: Session = Depends(database.get_db)):
     correct_key = settings.admin_key
     if token != "admin-session-valid" and token != correct_key:
         raise HTTPException(status_code=401, detail="Unauthorized")
     
     entry = db.query(models.PPDBRegistration).filter(models.PPDBRegistration.id == id).first()
     if not entry:
         raise HTTPException(status_code=404, detail="Data not found")
     
     db.delete(entry)
     db.commit()
     return {"success": True, "message": "Data deleted"}
