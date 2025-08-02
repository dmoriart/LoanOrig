"""
SQLite-compatible database models for the Loan Origination System
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import enum
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./loan_origination.db')

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum definitions
class UserRole(enum.Enum):
    APPLICANT = "applicant"
    UNDERWRITER = "underwriter"
    ADMIN = "admin"
    PROCESSOR = "processor"
    MANAGER = "manager"

class LoanStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FUNDED = "funded"
    CLOSED = "closed"

class EmploymentStatus(enum.Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"
    STUDENT = "student"

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)  # UUID as string for SQLite
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.APPLICANT)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    
    id = Column(String(36), primary_key=True)  # UUID as string for SQLite
    applicant_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    loan_number = Column(String(50), unique=True, nullable=False)
    
    # Loan Details
    loan_amount = Column(Numeric(12, 2), nullable=False)
    loan_purpose = Column(String(100), nullable=False)
    property_address = Column(Text)
    property_value = Column(Numeric(12, 2))
    down_payment = Column(Numeric(12, 2))
    
    # Personal Information
    annual_income = Column(Numeric(10, 2))
    employment_status = Column(Enum(EmploymentStatus))
    employer_name = Column(String(200))
    job_title = Column(String(100))
    years_employed = Column(Float)
    monthly_debt_payments = Column(Numeric(10, 2))
    
    # Application Status
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.DRAFT)
    submitted_at = Column(DateTime)
    decision_date = Column(DateTime)
    closing_date = Column(DateTime)
    
    # System fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applicant = relationship("User", foreign_keys=[applicant_id])

def get_database():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
