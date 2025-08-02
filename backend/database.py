from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum, Numeric, Date, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import enum
from dotenv import load_dotenv
import uuid

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/loan_origination')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Check if we're using SQLite for compatibility
IS_SQLITE = 'sqlite' in DATABASE_URL.lower()

# UUID type that works with both PostgreSQL and SQLite
if IS_SQLITE:
    from sqlalchemy import String as UUIDType
    JSON_TYPE = Text  # SQLite doesn't have JSON type
    INET_TYPE = String  # SQLite doesn't have INET type
else:
    UUIDType = UUID
    JSON_TYPE = JSONB
    INET_TYPE = INET

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

class DocumentStatus(enum.Enum):
    PENDING = "pending"
    UPLOADED = "uploaded"
    VERIFIED = "verified"
    REJECTED = "rejected"

class UnderwritingDecision(enum.Enum):
    APPROVE = "approve"
    REJECT = "reject"
    CONDITIONAL_APPROVAL = "conditional_approval"
    PENDING = "pending"
    REQUEST_MORE_INFO = "request_more_info"

class AssetType(enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    RETIREMENT = "retirement"
    REAL_ESTATE = "real_estate"
    VEHICLE = "vehicle"
    OTHER = "other"

class LiabilityType(enum.Enum):
    CREDIT_CARD = "credit_card"
    AUTO_LOAN = "auto_loan"
    MORTGAGE = "mortgage"
    STUDENT_LOAN = "student_loan"
    PERSONAL_LOAN = "personal_loan"
    OTHER = "other"

class IncomeType(enum.Enum):
    SALARY = "salary"
    HOURLY = "hourly"
    COMMISSION = "commission"
    BONUS = "bonus"
    SELF_EMPLOYMENT = "self_employment"
    RENTAL = "rental"
    INVESTMENT = "investment"
    OTHER = "other"

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.APPLICANT)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loan_applications = relationship("LoanApplication", back_populates="applicant", foreign_keys="LoanApplication.applicant_id")
    assigned_loans = relationship("LoanApplication", back_populates="assigned_underwriter", foreign_keys="LoanApplication.assigned_underwriter_id")
    documents = relationship("Document", back_populates="uploaded_by_user")
    underwriting_decisions = relationship("UnderwritingDecision", back_populates="underwriter")

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    loan_number = Column(String(50), unique=True, nullable=False)
    
    # Loan Details
    loan_amount = Column(Numeric(12, 2), nullable=False)
    loan_purpose = Column(String(100), nullable=False)
    property_address = Column(Text)
    property_value = Column(Numeric(12, 2))
    down_payment = Column(Numeric(12, 2), default=0)
    
    # Personal Information
    ssn = Column(String(11))
    date_of_birth = Column(Date)
    marital_status = Column(String(20))
    dependents = Column(Integer, default=0)
    
    # Contact Information
    current_address = Column(Text)
    previous_address = Column(Text)
    years_at_current_address = Column(Numeric(3, 1))
    
    # Employment Information
    employment_status = Column(Enum(EmploymentStatus))
    employer_name = Column(String(200))
    job_title = Column(String(100))
    years_with_employer = Column(Numeric(3, 1))
    employer_phone = Column(String(20))
    
    # Financial Summary
    monthly_income = Column(Numeric(10, 2))
    total_assets = Column(Numeric(12, 2))
    total_liabilities = Column(Numeric(12, 2))
    credit_score = Column(Integer)
    
    # Application Status
    status = Column(Enum(LoanStatus), default=LoanStatus.DRAFT)
    submitted_at = Column(DateTime(timezone=True))
    assigned_underwriter_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applicant = relationship("User", back_populates="loan_applications", foreign_keys=[applicant_id])
    assigned_underwriter = relationship("User", back_populates="assigned_loans", foreign_keys=[assigned_underwriter_id])
    income_records = relationship("ApplicantIncome", back_populates="application", cascade="all, delete-orphan")
    assets = relationship("ApplicantAsset", back_populates="application", cascade="all, delete-orphan")
    liabilities = relationship("ApplicantLiability", back_populates="application", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="application", cascade="all, delete-orphan")
    underwriting_decisions = relationship("UnderwritingDecision", back_populates="application", cascade="all, delete-orphan")
    workflow_status = relationship("WorkflowStatus", back_populates="application", cascade="all, delete-orphan")

class ApplicantIncome(Base):
    __tablename__ = "applicant_income"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    income_type = Column(Enum(IncomeType), nullable=False)
    source = Column(String(200), nullable=False)
    monthly_amount = Column(Numeric(10, 2), nullable=False)
    is_primary = Column(Boolean, default=False)
    years_receiving = Column(Numeric(3, 1))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="income_records")

class ApplicantAsset(Base):
    __tablename__ = "applicant_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    description = Column(String(200), nullable=False)
    current_value = Column(Numeric(12, 2), nullable=False)
    liquid_amount = Column(Numeric(12, 2), default=0)
    institution_name = Column(String(200))
    account_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="assets")

class ApplicantLiability(Base):
    __tablename__ = "applicant_liabilities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    liability_type = Column(Enum(LiabilityType), nullable=False)
    creditor_name = Column(String(200), nullable=False)
    current_balance = Column(Numeric(12, 2), nullable=False)
    monthly_payment = Column(Numeric(10, 2), nullable=False)
    remaining_months = Column(Integer)
    account_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="liabilities")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Document Details
    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100))
    
    # Document Status
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING)
    verified_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    verified_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    
    # Metadata
    description = Column(Text)
    is_required = Column(Boolean, default=False)
    expiration_date = Column(Date)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="documents")
    uploaded_by_user = relationship("User", back_populates="documents", foreign_keys=[uploaded_by])
    verified_by_user = relationship("User", foreign_keys=[verified_by])

class UnderwritingDecision(Base):
    __tablename__ = "underwriting_decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    underwriter_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Decision Details
    decision = Column(Enum(UnderwritingDecision), nullable=False)
    decision_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    conditions = Column(Text)
    notes = Column(Text)
    
    # Loan Terms (if approved)
    approved_amount = Column(Numeric(12, 2))
    interest_rate = Column(Numeric(5, 3))
    loan_term_months = Column(Integer)
    
    # Risk Assessment
    debt_to_income_ratio = Column(Numeric(5, 2))
    loan_to_value_ratio = Column(Numeric(5, 2))
    risk_score = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="underwriting_decisions")
    underwriter = relationship("User", back_populates="underwriting_decisions")

class WorkflowStatus(Base):
    __tablename__ = "workflow_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey('loan_applications.id'), nullable=False)
    status = Column(String(50), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Status Details
    step_name = Column(String(100), nullable=False)
    step_order = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    
    # Notes and Comments
    comments = Column(Text)
    internal_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = relationship("LoanApplication", back_populates="workflow_status")
    assigned_user = relationship("User", foreign_keys=[assigned_to])

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Who did what
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user_email = Column(String(255))
    user_role = Column(Enum(UserRole))
    
    # What was done
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True))
    
    # Details
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    change_summary = Column(Text)
    
    # Context
    ip_address = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(255))
    
    # Compliance
    regulation_reference = Column(String(100))
    compliance_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])

class SystemSetting(Base):
    __tablename__ = "system_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    is_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
