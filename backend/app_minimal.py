"""
Ultra-minimal FastAPI app for Render deployment
Absolute minimum dependencies to avoid any build issues
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

# Create FastAPI app
app = FastAPI(
    title="Loan Origination API", 
    version="1.0.0",
    description="Minimal loan origination system API for deployment testing"
)

# CORS headers middleware
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

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

# In-memory loan storage for demo
LOANS = [
    {
        "id": 1,
        "applicant_name": "John Doe",
        "loan_amount": 250000.00,
        "income": 75000.00,
        "employment_status": "employed",
        "status": "approved",
        "application_date": "2025-08-01",
        "credit_score": 720,
        "purpose": "home_purchase"
    },
    {
        "id": 2,
        "applicant_name": "Jane Smith",
        "loan_amount": 180000.00,
        "income": 65000.00,
        "employment_status": "employed",
        "status": "under_review",
        "application_date": "2025-08-02",
        "credit_score": 750,
        "purpose": "refinance"
    }
]

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Loan Origination System API",
        "status": "running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "loan-origination-api",
        "version": "1.0.0"
    }

# Get all loans
@app.get("/api/v1/loans", response_model=List[LoanResponse])
async def get_loans():
    return LOANS

# Create loan
@app.post("/api/v1/loans", response_model=LoanResponse)
async def create_loan(loan: LoanApplication):
    new_loan = {
        "id": len(LOANS) + 1,
        "applicant_name": loan.applicant_name,
        "loan_amount": loan.loan_amount,
        "income": loan.income,
        "employment_status": loan.employment_status,
        "status": "submitted",
        "application_date": "2025-08-03",
        "credit_score": loan.credit_score,
        "purpose": loan.purpose
    }
    LOANS.append(new_loan)
    return new_loan

# Get loan by ID
@app.get("/api/v1/loans/{loan_id}", response_model=LoanResponse)
async def get_loan(loan_id: int):
    for loan in LOANS:
        if loan["id"] == loan_id:
            return loan
    raise HTTPException(status_code=404, detail="Loan not found")

# Loan statistics
@app.get("/api/v1/stats")
async def get_stats():
    total = len(LOANS)
    total_amount = sum(loan["loan_amount"] for loan in LOANS)
    avg_income = sum(loan["income"] for loan in LOANS) / total if total > 0 else 0
    
    return {
        "total_applications": total,
        "total_loan_amount": total_amount,
        "average_income": round(avg_income, 2),
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
