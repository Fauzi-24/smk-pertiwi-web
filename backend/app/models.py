from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    slug = Column(String, unique=True, index=True)
    image_url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=True)
    
    author = relationship("User")

class PPDBStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class PPDBRegistration(Base):
    __tablename__ = "ppdb_registrations"

    id = Column(Integer, primary_key=True, index=True)
    nisn = Column(String, unique=True, index=True)
    full_name = Column(String)
    place_of_birth = Column(String)
    date_of_birth = Column(String)
    gender = Column(String)
    religion = Column(String)
    school_origin = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    
    father_name = Column(String)
    father_job = Column(String)
    mother_name = Column(String)
    mother_job = Column(String)
    parent_phone = Column(String)
    parent_income = Column(String)
    parent_address = Column(Text)
    
    major_choice = Column(String)
    graduation_year = Column(Integer)
    average_score = Column(String, nullable=True)
    
    status = Column(String, default=PPDBStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    correction = Column(Text)
    source = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)
