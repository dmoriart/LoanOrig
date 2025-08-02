from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Basic health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "loan-origination-flask"})

# Loan application endpoints
@app.route('/api/loans', methods=['GET'])
def get_loans():
    # Mock data for now - replace with database queries
    loans = [
        {
            "id": 1,
            "applicant_name": "John Doe",
            "loan_amount": 250000,
            "status": "pending",
            "application_date": "2024-01-15"
        },
        {
            "id": 2,
            "applicant_name": "Jane Smith",
            "loan_amount": 150000,
            "status": "approved",
            "application_date": "2024-01-10"
        }
    ]
    return jsonify(loans)

@app.route('/api/loans', methods=['POST'])
def create_loan_application():
    data = request.get_json()
    
    # Basic validation
    required_fields = ['applicant_name', 'loan_amount', 'income', 'employment_status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Mock response - replace with database insert
    new_loan = {
        "id": 3,
        "applicant_name": data['applicant_name'],
        "loan_amount": data['loan_amount'],
        "income": data['income'],
        "employment_status": data['employment_status'],
        "status": "pending",
        "application_date": "2024-01-20"
    }
    
    return jsonify(new_loan), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
