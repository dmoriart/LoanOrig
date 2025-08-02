from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from database_sqlite import SessionLocal, User, LoanApplication as LoanApplicationModel
from sqlalchemy.orm import Session

load_dotenv()

app = FastAPI(title="Loan Origination API", version="1.0.0")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoanApplication(BaseModel):
    applicant_name: str
    loan_amount: float
    income: float
    employment_status: str
    credit_score: Optional[int] = None
    purpose: Optional[str] = None

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    loan_amount: float
    income: float
    employment_status: str
    status: str
    application_date: str
    credit_score: Optional[int] = None
    purpose: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "loan-origination-fastapi"}

# Loan endpoints
@app.get("/api/v1/loans")
async def get_loans(db: Session = Depends(get_db)):
    """Get all loan applications"""
    loans = db.query(LoanApplicationModel).all()
    return [
        {
            "id": loan.id,
            "loan_number": loan.loan_number,
            "applicant_name": f"{loan.applicant.first_name} {loan.applicant.last_name}" if loan.applicant else "Unknown",
            "loan_amount": float(loan.loan_amount),
            "annual_income": float(loan.annual_income) if loan.annual_income else 0,
            "employment_status": loan.employment_status.value if loan.employment_status else "unknown",
            "status": loan.status.value,
            "application_date": loan.created_at.isoformat() if loan.created_at else None,
            "purpose": loan.loan_purpose
        }
        for loan in loans
    ]

@app.get("/api/v1/loans/{loan_id}")
async def get_loan(loan_id: str, db: Session = Depends(get_db)):
    """Get a specific loan application"""
    loan = db.query(LoanApplicationModel).filter(LoanApplicationModel.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan application not found")
    
    return {
        "id": loan.id,
        "loan_number": loan.loan_number,
        "applicant_name": f"{loan.applicant.first_name} {loan.applicant.last_name}" if loan.applicant else "Unknown",
        "loan_amount": float(loan.loan_amount),
        "annual_income": float(loan.annual_income) if loan.annual_income else 0,
        "employment_status": loan.employment_status.value if loan.employment_status else "unknown",
        "employer_name": loan.employer_name,
        "job_title": loan.job_title,
        "property_address": loan.property_address,
        "property_value": float(loan.property_value) if loan.property_value else 0,
        "down_payment": float(loan.down_payment) if loan.down_payment else 0,
        "status": loan.status.value,
        "application_date": loan.created_at.isoformat() if loan.created_at else None,
        "purpose": loan.loan_purpose
    }

@app.post("/api/v1/loans", response_model=LoanResponse)
async def create_loan_application(loan: LoanApplication):
    # Mock response - replace with database insert
    new_loan = {
        "id": 3,
        "applicant_name": loan.applicant_name,
        "loan_amount": loan.loan_amount,
        "income": loan.income,
        "employment_status": loan.employment_status,
        "status": "pending",
        "application_date": "2024-01-20",
        "credit_score": loan.credit_score,
        "purpose": loan.purpose
    }
    return new_loan

@app.get("/api/v1/loans/{loan_id}", response_model=LoanResponse)
async def get_loan(loan_id: int):
    # Mock response - replace with database query
    if loan_id == 1:
        return {
            "id": 1,
            "applicant_name": "John Doe",
            "loan_amount": 250000.00,
            "income": 75000.00,
            "employment_status": "employed",
            "status": "pending",
            "application_date": "2024-01-15",
            "credit_score": 720,
            "purpose": "home_purchase"
        }
    else:
        raise HTTPException(status_code=404, detail="Loan not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
