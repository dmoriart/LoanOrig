"""
Seed data for the Loan Origination System
Run this script to populate the database with initial test data
"""

from database import SessionLocal, User, LoanApplication, SystemSetting, UserRole, LoanStatus, EmploymentStatus
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid
from datetime import datetime, date
from decimal import Decimal

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Seed data already exists. Skipping...")
            return
        
        print("Creating seed data...")
        
        # Create system settings
        settings = [
            SystemSetting(
                setting_key="max_loan_amount",
                setting_value="2000000",
                description="Maximum loan amount allowed"
            ),
            SystemSetting(
                setting_key="min_credit_score",
                setting_value="620",
                description="Minimum credit score required"
            ),
            SystemSetting(
                setting_key="max_dti_ratio",
                setting_value="43",
                description="Maximum debt-to-income ratio allowed"
            ),
            SystemSetting(
                setting_key="document_retention_days",
                setting_value="2555",
                description="Days to retain documents (7 years)"
            ),
            SystemSetting(
                setting_key="session_timeout_minutes",
                setting_value="30",
                description="User session timeout in minutes"
            )
        ]
        
        for setting in settings:
            db.add(setting)
        
        # Create users
        users_data = [
            {
                "email": "admin@loanorigination.com",
                "password": "admin123",
                "first_name": "System",
                "last_name": "Administrator",
                "role": UserRole.ADMIN,
                "phone": "+1-555-0100",
                "email_verified": True
            },
            {
                "email": "underwriter@loanorigination.com",
                "password": "underwriter123",
                "first_name": "John",
                "last_name": "Underwriter",
                "role": UserRole.UNDERWRITER,
                "phone": "+1-555-0101",
                "email_verified": True
            },
            {
                "email": "processor@loanorigination.com",
                "password": "processor123",
                "first_name": "Jane",
                "last_name": "Processor",
                "role": UserRole.PROCESSOR,
                "phone": "+1-555-0102",
                "email_verified": True
            },
            {
                "email": "john.doe@email.com",
                "password": "applicant123",
                "first_name": "John",
                "last_name": "Doe",
                "role": UserRole.APPLICANT,
                "phone": "+1-555-0201",
                "email_verified": True
            },
            {
                "email": "jane.smith@email.com",
                "password": "applicant123",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": UserRole.APPLICANT,
                "phone": "+1-555-0202",
                "email_verified": True
            }
        ]
        
        created_users = {}
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                phone=user_data["phone"],
                email_verified=user_data["email_verified"]
            )
            db.add(user)
            db.flush()  # Get the ID
            created_users[user_data["email"]] = user
        
        # Create sample loan applications
        loan_applications_data = [
            {
                "applicant_email": "john.doe@email.com",
                "loan_number": "LN-2025-000001",
                "loan_amount": Decimal("250000.00"),
                "loan_purpose": "Home Purchase",
                "property_address": "123 Main St, Anytown, ST 12345",
                "property_value": Decimal("300000.00"),
                "down_payment": Decimal("50000.00"),
                "ssn": "123-45-6789",
                "date_of_birth": date(1985, 6, 15),
                "marital_status": "Married",
                "dependents": 2,
                "current_address": "456 Current Ave, Anytown, ST 12345",
                "years_at_current_address": Decimal("3.5"),
                "employment_status": EmploymentStatus.EMPLOYED,
                "employer_name": "Tech Corp Inc",
                "job_title": "Software Engineer",
                "years_with_employer": Decimal("4.2"),
                "employer_phone": "+1-555-1234",
                "monthly_income": Decimal("8500.00"),
                "total_assets": Decimal("125000.00"),
                "total_liabilities": Decimal("35000.00"),
                "credit_score": 740,
                "status": LoanStatus.SUBMITTED,
                "submitted_at": datetime.utcnow()
            },
            {
                "applicant_email": "jane.smith@email.com",
                "loan_number": "LN-2025-000002",
                "loan_amount": Decimal("180000.00"),
                "loan_purpose": "Refinance",
                "property_address": "789 Oak St, Somewhere, ST 54321",
                "property_value": Decimal("220000.00"),
                "ssn": "987-65-4321",
                "date_of_birth": date(1980, 3, 22),
                "marital_status": "Single",
                "dependents": 1,
                "current_address": "789 Oak St, Somewhere, ST 54321",
                "years_at_current_address": Decimal("7.0"),
                "employment_status": EmploymentStatus.EMPLOYED,
                "employer_name": "Healthcare Systems",
                "job_title": "Nurse Practitioner",
                "years_with_employer": Decimal("6.5"),
                "employer_phone": "+1-555-5678",
                "monthly_income": Decimal("7200.00"),
                "total_assets": Decimal("95000.00"),
                "total_liabilities": Decimal("42000.00"),
                "credit_score": 720,
                "status": LoanStatus.UNDER_REVIEW,
                "submitted_at": datetime.utcnow(),
                "assigned_underwriter_id": created_users["underwriter@loanorigination.com"].id
            }
        ]
        
        for app_data in loan_applications_data:
            applicant = created_users[app_data["applicant_email"]]
            app_data_copy = app_data.copy()
            del app_data_copy["applicant_email"]
            
            loan_app = LoanApplication(
                applicant_id=applicant.id,
                **app_data_copy
            )
            db.add(loan_app)
        
        db.commit()
        print("Seed data created successfully!")
        
        # Print created users for reference
        print("\nCreated users:")
        print("=" * 50)
        for email, user in created_users.items():
            print(f"Email: {email}")
            print(f"Role: {user.role.value}")
            print(f"Password: {users_data[list(created_users.keys()).index(email)]['password']}")
            print("-" * 30)
            
    except Exception as e:
        db.rollback()
        print(f"Error creating seed data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()
