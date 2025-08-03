"""
Production FastAPI app for Render deployment
Ultra-minimal version to avoid any compilation issues
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Loan Origination API", 
    version="1.0.0",
    description="Production loan origination system API"
)

# Simple CORS - no external dependencies
@app.middleware("http")
async def cors_handler(request, call_next):
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

class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    database_url: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "service": "loan-origination-fastapi",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_url": "configured" if os.getenv("DATABASE_URL") else "not_configured"
    }

# Mock loan data for production demo
MOCK_LOANS = [
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
    },
    {
        "id": 3,
        "applicant_name": "Mike Johnson",
        "loan_amount": 320000.00,
        "income": 95000.00,
        "employment_status": "self_employed",
        "status": "pending",
        "application_date": "2025-08-03",
        "credit_score": 680,
        "purpose": "home_purchase"
    }
]

# Loan endpoints
@app.get("/api/v1/loans", response_model=List[LoanResponse])
async def get_loans():
    """Get all loan applications"""
    return MOCK_LOANS

@app.post("/api/v1/loans", response_model=LoanResponse)
async def create_loan_application(loan: LoanApplication):
    """Create a new loan application"""
    new_loan = {
        "id": len(MOCK_LOANS) + 1,
        "applicant_name": loan.applicant_name,
        "loan_amount": loan.loan_amount,
        "income": loan.income,
        "employment_status": loan.employment_status,
        "status": "submitted",
        "application_date": "2025-08-03",
        "credit_score": loan.credit_score,
        "purpose": loan.purpose
    }
    MOCK_LOANS.append(new_loan)
    return new_loan

@app.get("/api/v1/loans/{loan_id}", response_model=LoanResponse)
async def get_loan(loan_id: int):
    """Get a specific loan application by ID"""
    for loan in MOCK_LOANS:
        if loan["id"] == loan_id:
            return loan
    raise HTTPException(status_code=404, detail="Loan not found")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Loan Origination System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Add some additional endpoints for demonstration
@app.get("/api/v1/stats")
async def get_loan_stats():
    """Get loan application statistics"""
    total_loans = len(MOCK_LOANS)
    total_amount = sum(loan["loan_amount"] for loan in MOCK_LOANS)
    avg_credit_score = sum(loan["credit_score"] or 0 for loan in MOCK_LOANS) / total_loans
    
    status_counts = {}
    for loan in MOCK_LOANS:
        status = loan["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "total_applications": total_loans,
        "total_loan_amount": total_amount,
        "average_credit_score": round(avg_credit_score, 2),
        "status_breakdown": status_counts
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
