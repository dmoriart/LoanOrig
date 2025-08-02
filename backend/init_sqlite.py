#!/usr/bin/env python3
"""
SQLite Database initialization script
"""
import uuid
from database_sqlite import Base, engine, SessionLocal, User, LoanApplication, UserRole, LoanStatus, EmploymentStatus
from datetime import datetime

def init_database():
    """Initialize SQLite database with tables and sample data"""
    print("🏦 Initializing SQLite Database")
    print("=" * 40)
    
    try:
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Create sample data
        print("🌱 Creating sample data...")
        db = SessionLocal()
        
        # Create sample user
        user_id = str(uuid.uuid4())
        sample_user = User(
            id=user_id,
            email="john.doe@example.com",
            password_hash="$2b$12$LQv3c1yqBWVHoNKjAx/x7u1aP7R9QQrUQh2h3K9dN7xV8Y5Z9w1bC",  # "password123"
            first_name="John",
            last_name="Doe",
            phone="555-0123",
            role=UserRole.APPLICANT
        )
        db.add(sample_user)
        
        # Create sample loan application
        loan_id = str(uuid.uuid4())
        sample_loan = LoanApplication(
            id=loan_id,
            applicant_id=user_id,
            loan_number="LN-2025-001",
            loan_amount=250000.00,
            loan_purpose="Home Purchase",
            property_address="123 Main St, Anytown, ST 12345",
            property_value=300000.00,
            down_payment=50000.00,
            annual_income=75000.00,
            employment_status=EmploymentStatus.EMPLOYED,
            employer_name="Tech Corp",
            job_title="Software Developer",
            years_employed=3.5,
            monthly_debt_payments=1200.00,
            status=LoanStatus.SUBMITTED,
            submitted_at=datetime.utcnow()
        )
        db.add(sample_loan)
        
        db.commit()
        print("✅ Sample data created!")
        
        # Verify data
        user_count = db.query(User).count()
        loan_count = db.query(LoanApplication).count()
        print(f"📊 Database initialized with {user_count} users and {loan_count} loan applications")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    if init_database():
        print("\n🎉 Database initialization complete!")
        print("\n📋 Next steps:")
        print("1. Start FastAPI server: python fastapi_app.py")
        print("2. Test at: http://localhost:8000/docs")
        print("3. View sample data at: http://localhost:8000/api/v1/loans")
    else:
        print("\n❌ Database initialization failed!")
