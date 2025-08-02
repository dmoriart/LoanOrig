# 🔧 Manual Database Setup for Supabase
## Alternative Setup Method

Since there's a psycopg2 compatibility issue on your system, let's set up the database manually using Supabase's SQL editor.

## Step 1: Access Supabase SQL Editor

1. Go to: https://kjbiltokwmrelyyvrnmu.supabase.co
2. Sign in to your Supabase account
3. Navigate to **SQL Editor** (in the left sidebar)

## Step 2: Create the Database Schema

Copy and paste the following SQL script into the SQL editor and run it:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom ENUM types
CREATE TYPE user_role AS ENUM ('applicant', 'underwriter', 'admin', 'processor', 'manager');
CREATE TYPE loan_status AS ENUM ('draft', 'submitted', 'under_review', 'approved', 'rejected', 'funded', 'closed');
CREATE TYPE employment_status AS ENUM ('employed', 'self_employed', 'unemployed', 'retired', 'student');
CREATE TYPE document_status AS ENUM ('pending', 'uploaded', 'verified', 'rejected');
CREATE TYPE underwriting_decision AS ENUM ('approve', 'reject', 'conditional_approval', 'pending', 'request_more_info');
CREATE TYPE asset_type AS ENUM ('checking', 'savings', 'investment', 'retirement', 'real_estate', 'vehicle', 'other');
CREATE TYPE liability_type AS ENUM ('credit_card', 'auto_loan', 'mortgage', 'student_loan', 'personal_loan', 'other');
CREATE TYPE income_type AS ENUM ('salary', 'hourly', 'commission', 'bonus', 'self_employment', 'rental', 'investment', 'other');

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role user_role NOT NULL DEFAULT 'applicant',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Loan applications table
CREATE TABLE loan_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    applicant_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    loan_number VARCHAR(50) UNIQUE NOT NULL,
    loan_amount DECIMAL(12,2) NOT NULL CHECK (loan_amount > 0),
    loan_purpose VARCHAR(100) NOT NULL,
    property_address TEXT,
    property_value DECIMAL(12,2),
    down_payment DECIMAL(12,2) DEFAULT 0,
    ssn VARCHAR(11),
    date_of_birth DATE,
    marital_status VARCHAR(20),
    dependents INTEGER DEFAULT 0,
    current_address TEXT,
    previous_address TEXT,
    years_at_current_address DECIMAL(3,1),
    employment_status employment_status,
    employer_name VARCHAR(200),
    job_title VARCHAR(100),
    years_with_employer DECIMAL(3,1),
    employer_phone VARCHAR(20),
    monthly_income DECIMAL(10,2),
    total_assets DECIMAL(12,2),
    total_liabilities DECIMAL(12,2),
    credit_score INTEGER CHECK (credit_score BETWEEN 300 AND 850),
    status loan_status DEFAULT 'draft',
    submitted_at TIMESTAMP WITH TIME ZONE,
    assigned_underwriter_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Financial data tables
CREATE TABLE applicant_income (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    income_type income_type NOT NULL,
    source VARCHAR(200) NOT NULL,
    monthly_amount DECIMAL(10,2) NOT NULL CHECK (monthly_amount >= 0),
    is_primary BOOLEAN DEFAULT FALSE,
    years_receiving DECIMAL(3,1),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applicant_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    asset_type asset_type NOT NULL,
    description VARCHAR(200) NOT NULL,
    current_value DECIMAL(12,2) NOT NULL CHECK (current_value >= 0),
    liquid_amount DECIMAL(12,2) DEFAULT 0,
    institution_name VARCHAR(200),
    account_number VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applicant_liabilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    liability_type liability_type NOT NULL,
    creditor_name VARCHAR(200) NOT NULL,
    current_balance DECIMAL(12,2) NOT NULL CHECK (current_balance >= 0),
    monthly_payment DECIMAL(10,2) NOT NULL CHECK (monthly_payment >= 0),
    remaining_months INTEGER,
    account_number VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    uploaded_by UUID NOT NULL REFERENCES users(id),
    document_type VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    status document_status DEFAULT 'pending',
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMP WITH TIME ZONE,
    rejection_reason TEXT,
    description TEXT,
    is_required BOOLEAN DEFAULT FALSE,
    expiration_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Underwriting decisions table
CREATE TABLE underwriting_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    underwriter_id UUID NOT NULL REFERENCES users(id),
    decision underwriting_decision NOT NULL,
    decision_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    conditions TEXT,
    notes TEXT,
    approved_amount DECIMAL(12,2),
    interest_rate DECIMAL(5,3),
    loan_term_months INTEGER,
    debt_to_income_ratio DECIMAL(5,2),
    loan_to_value_ratio DECIMAL(5,2),
    risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflow status table
CREATE TABLE workflow_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    assigned_to UUID REFERENCES users(id),
    step_name VARCHAR(100) NOT NULL,
    step_order INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    due_date TIMESTAMP WITH TIME ZONE,
    comments TEXT,
    internal_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    user_email VARCHAR(255),
    user_role user_role,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    change_summary TEXT,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    regulation_reference VARCHAR(100),
    compliance_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System settings table
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_loan_applications_applicant ON loan_applications(applicant_id);
CREATE INDEX idx_loan_applications_status ON loan_applications(status);
CREATE INDEX idx_documents_application ON documents(application_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('max_loan_amount', '2000000', 'Maximum loan amount allowed'),
('min_credit_score', '620', 'Minimum credit score required'),
('max_dti_ratio', '43', 'Maximum debt-to-income ratio allowed');

-- Insert default admin user (password: admin123)
INSERT INTO users (email, password_hash, first_name, last_name, role, email_verified) VALUES
('admin@loanorigination.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewfBuX4/nG/9e.72', 'System', 'Administrator', 'admin', TRUE);

SELECT 'Database setup completed successfully!' as status;
```

## Step 3: Verify Setup

After running the SQL script, you should see:
- ✅ All tables created
- ✅ Indexes added
- ✅ Default admin user created
- ✅ System settings configured

## Step 4: Test Your Application

Now you can start your FastAPI server to test the connection:

```bash
cd backend
python fastapi_app.py
```

Then visit: http://localhost:8000/docs

## Alternative: Try Different Database Driver

If you want to fix the psycopg2 issue, you can try:

```bash
# Option 1: Use Homebrew PostgreSQL
brew install postgresql
pip install psycopg2

# Option 2: Use asyncpg (for async operations)
pip install asyncpg

# Option 3: Use pg8000 (pure Python driver)
pip install pg8000
```

## Troubleshooting

If you encounter issues:
1. Check the **Logs** tab in Supabase for any SQL errors
2. Verify your database password is correct
3. Ensure your Supabase project is active
4. Try refreshing the SQL editor page

Once the database is set up manually, your FastAPI application should work correctly with the Supabase database!
