"""
Pure Python WSGI app for Render deployment
Uses only standard library + gunicorn to avoid ALL compilation issues
"""
import json
import os
from urllib.parse import parse_qs

# Sample loan data
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

def application(environ, start_response):
    """WSGI application"""
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # CORS headers
    headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
        ('Access-Control-Allow-Headers', '*'),
        ('Content-Type', 'application/json')
    ]
    
    # Handle OPTIONS requests (CORS preflight)
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']
    
    # Route handling
    if path == '/' or path == '':
        response = {
            "message": "Loan Origination System API",
            "status": "running",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production")
        }
        start_response('200 OK', headers)
        return [json.dumps(response).encode('utf-8')]
    
    elif path == '/health':
        response = {
            "status": "healthy",
            "service": "loan-origination-api",
            "version": "1.0.0"
        }
        start_response('200 OK', headers)
        return [json.dumps(response).encode('utf-8')]
    
    elif path == '/api/v1/loans':
        if method == 'GET':
            response = {"loans": LOANS, "count": len(LOANS)}
            start_response('200 OK', headers)
            return [json.dumps(response).encode('utf-8')]
        
        elif method == 'POST':
            # Simple POST handling
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                if content_length > 0:
                    post_data = environ['wsgi.input'].read(content_length)
                    loan_data = json.loads(post_data.decode('utf-8'))
                else:
                    loan_data = {}
                
                new_loan = {
                    "id": len(LOANS) + 1,
                    "applicant_name": loan_data.get("applicant_name", "Unknown"),
                    "loan_amount": loan_data.get("loan_amount", 0),
                    "income": loan_data.get("income", 0),
                    "employment_status": loan_data.get("employment_status", "unknown"),
                    "status": "submitted",
                    "application_date": "2025-08-03",
                    "credit_score": loan_data.get("credit_score"),
                    "purpose": loan_data.get("purpose")
                }
                LOANS.append(new_loan)
                
                start_response('201 Created', headers)
                return [json.dumps(new_loan).encode('utf-8')]
            except Exception as e:
                error_response = {"error": "Invalid request data", "detail": str(e)}
                start_response('400 Bad Request', headers)
                return [json.dumps(error_response).encode('utf-8')]
    
    elif path.startswith('/api/v1/loans/'):
        try:
            loan_id = int(path.split('/')[-1])
            for loan in LOANS:
                if loan["id"] == loan_id:
                    start_response('200 OK', headers)
                    return [json.dumps(loan).encode('utf-8')]
            
            error_response = {"error": "Loan not found"}
            start_response('404 Not Found', headers)
            return [json.dumps(error_response).encode('utf-8')]
        except ValueError:
            error_response = {"error": "Invalid loan ID"}
            start_response('400 Bad Request', headers)
            return [json.dumps(error_response).encode('utf-8')]
    
    elif path == '/api/v1/stats':
        total = len(LOANS)
        total_amount = sum(loan["loan_amount"] for loan in LOANS)
        avg_income = sum(loan["income"] for loan in LOANS) / total if total > 0 else 0
        
        response = {
            "total_applications": total,
            "total_loan_amount": total_amount,
            "average_income": round(avg_income, 2),
            "api_version": "1.0.0"
        }
        start_response('200 OK', headers)
        return [json.dumps(response).encode('utf-8')]
    
    # 404 for unknown paths
    error_response = {"error": "Not found", "path": path}
    start_response('404 Not Found', headers)
    return [json.dumps(error_response).encode('utf-8')]

# For direct testing
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting WSGI server on port {port}")
    
    server = make_server('0.0.0.0', port, application)
    server.serve_forever()
