-- Comprehensive Loan Origination System Database Schema
-- PostgreSQL Migration Script v1.0
-- Created: August 2025

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

-- ======================
-- USERS TABLE
-- ======================
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

-- ======================
-- LOAN APPLICATIONS TABLE
-- ======================
CREATE TABLE loan_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    applicant_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    loan_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Loan Details
    loan_amount DECIMAL(12,2) NOT NULL CHECK (loan_amount > 0),
    loan_purpose VARCHAR(100) NOT NULL,
    property_address TEXT,
    property_value DECIMAL(12,2),
    down_payment DECIMAL(12,2) DEFAULT 0,
    
    -- Personal Information
    ssn VARCHAR(11), -- Format: XXX-XX-XXXX
    date_of_birth DATE,
    marital_status VARCHAR(20),
    dependents INTEGER DEFAULT 0,
    
    -- Contact Information
    current_address TEXT,
    previous_address TEXT,
    years_at_current_address DECIMAL(3,1),
    
    -- Employment Information
    employment_status employment_status,
    employer_name VARCHAR(200),
    job_title VARCHAR(100),
    years_with_employer DECIMAL(3,1),
    employer_phone VARCHAR(20),
    
    -- Financial Summary
    monthly_income DECIMAL(10,2),
    total_assets DECIMAL(12,2),
    total_liabilities DECIMAL(12,2),
    credit_score INTEGER CHECK (credit_score BETWEEN 300 AND 850),
    
    -- Application Status
    status loan_status DEFAULT 'draft',
    submitted_at TIMESTAMP WITH TIME ZONE,
    assigned_underwriter_id UUID REFERENCES users(id),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- FINANCIAL DATA TABLES
-- ======================

-- Income Table
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

-- Assets Table
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

-- Liabilities Table
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

-- ======================
-- DOCUMENTS TABLE
-- ======================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    uploaded_by UUID NOT NULL REFERENCES users(id),
    
    -- Document Details
    document_type VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    
    -- Document Status
    status document_status DEFAULT 'pending',
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMP WITH TIME ZONE,
    rejection_reason TEXT,
    
    -- Metadata
    description TEXT,
    is_required BOOLEAN DEFAULT FALSE,
    expiration_date DATE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- UNDERWRITING WORKFLOW
-- ======================
CREATE TABLE underwriting_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    underwriter_id UUID NOT NULL REFERENCES users(id),
    
    -- Decision Details
    decision underwriting_decision NOT NULL,
    decision_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    conditions TEXT,
    notes TEXT,
    
    -- Loan Terms (if approved)
    approved_amount DECIMAL(12,2),
    interest_rate DECIMAL(5,3),
    loan_term_months INTEGER,
    
    -- Risk Assessment
    debt_to_income_ratio DECIMAL(5,2),
    loan_to_value_ratio DECIMAL(5,2),
    risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflow Status Tracking
CREATE TABLE workflow_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES loan_applications(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    assigned_to UUID REFERENCES users(id),
    
    -- Status Details
    step_name VARCHAR(100) NOT NULL,
    step_order INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    due_date TIMESTAMP WITH TIME ZONE,
    
    -- Notes and Comments
    comments TEXT,
    internal_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- AUDIT LOGS FOR COMPLIANCE
-- ======================
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Who did what
    user_id UUID REFERENCES users(id),
    user_email VARCHAR(255),
    user_role user_role,
    
    -- What was done
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- 'loan_application', 'document', 'user', etc.
    entity_id UUID,
    
    -- Details
    old_values JSONB,
    new_values JSONB,
    change_summary TEXT,
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    
    -- Compliance
    regulation_reference VARCHAR(100), -- TRID, HMDA, etc.
    compliance_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- SYSTEM CONFIGURATION
-- ======================
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- INDEXES FOR PERFORMANCE
-- ======================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Loan Applications indexes
CREATE INDEX idx_loan_applications_applicant ON loan_applications(applicant_id);
CREATE INDEX idx_loan_applications_status ON loan_applications(status);
CREATE INDEX idx_loan_applications_underwriter ON loan_applications(assigned_underwriter_id);
CREATE INDEX idx_loan_applications_submitted ON loan_applications(submitted_at);
CREATE INDEX idx_loan_applications_number ON loan_applications(loan_number);

-- Financial data indexes
CREATE INDEX idx_income_application ON applicant_income(application_id);
CREATE INDEX idx_assets_application ON applicant_assets(application_id);
CREATE INDEX idx_liabilities_application ON applicant_liabilities(application_id);

-- Documents indexes
CREATE INDEX idx_documents_application ON documents(application_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_uploaded_by ON documents(uploaded_by);

-- Underwriting indexes
CREATE INDEX idx_underwriting_application ON underwriting_decisions(application_id);
CREATE INDEX idx_underwriting_underwriter ON underwriting_decisions(underwriter_id);
CREATE INDEX idx_underwriting_decision ON underwriting_decisions(decision);

-- Workflow indexes
CREATE INDEX idx_workflow_application ON workflow_status(application_id);
CREATE INDEX idx_workflow_assigned ON workflow_status(assigned_to);
CREATE INDEX idx_workflow_status ON workflow_status(status);
CREATE INDEX idx_workflow_completed ON workflow_status(is_completed);

-- Audit logs indexes
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at);

-- ======================
-- TRIGGERS FOR UPDATED_AT
-- ======================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_loan_applications_updated_at BEFORE UPDATE ON loan_applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_workflow_status_updated_at BEFORE UPDATE ON workflow_status FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ======================
-- FUNCTIONS FOR BUSINESS LOGIC
-- ======================

-- Function to generate loan numbers
CREATE OR REPLACE FUNCTION generate_loan_number()
RETURNS VARCHAR(50) AS $$
DECLARE
    loan_number VARCHAR(50);
    counter INTEGER;
BEGIN
    -- Generate loan number with format: LN-YYYY-NNNNNN
    SELECT COALESCE(MAX(CAST(SUBSTRING(loan_number FROM 9) AS INTEGER)), 0) + 1
    INTO counter
    FROM loan_applications
    WHERE loan_number LIKE 'LN-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-%';
    
    loan_number := 'LN-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-' || LPAD(counter::TEXT, 6, '0');
    RETURN loan_number;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate debt-to-income ratio
CREATE OR REPLACE FUNCTION calculate_dti_ratio(application_uuid UUID)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    total_monthly_income DECIMAL(10,2);
    total_monthly_debt DECIMAL(10,2);
    dti_ratio DECIMAL(5,2);
BEGIN
    -- Get total monthly income
    SELECT COALESCE(SUM(monthly_amount), 0)
    INTO total_monthly_income
    FROM applicant_income
    WHERE application_id = application_uuid;
    
    -- Get total monthly debt payments
    SELECT COALESCE(SUM(monthly_payment), 0)
    INTO total_monthly_debt
    FROM applicant_liabilities
    WHERE application_id = application_uuid;
    
    -- Calculate DTI ratio
    IF total_monthly_income > 0 THEN
        dti_ratio := (total_monthly_debt / total_monthly_income) * 100;
    ELSE
        dti_ratio := 0;
    END IF;
    
    RETURN dti_ratio;
END;
$$ LANGUAGE plpgsql;

-- ======================
-- INITIAL SYSTEM DATA
-- ======================

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('max_loan_amount', '2000000', 'Maximum loan amount allowed'),
('min_credit_score', '620', 'Minimum credit score required'),
('max_dti_ratio', '43', 'Maximum debt-to-income ratio allowed'),
('document_retention_days', '2555', 'Days to retain documents (7 years)'),
('session_timeout_minutes', '30', 'User session timeout in minutes');

-- Insert default admin user (password should be changed immediately)
INSERT INTO users (email, password_hash, first_name, last_name, role, email_verified) VALUES
('admin@loanorigination.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewfBuX4/nG/9e.72', 'System', 'Administrator', 'admin', TRUE);

-- Add comments to tables for documentation
COMMENT ON TABLE users IS 'System users including applicants, underwriters, and administrators';
COMMENT ON TABLE loan_applications IS 'Main loan application data with personal and financial information';
COMMENT ON TABLE applicant_income IS 'Detailed income information for loan applicants';
COMMENT ON TABLE applicant_assets IS 'Asset information including bank accounts, investments, real estate';
COMMENT ON TABLE applicant_liabilities IS 'Debt and liability information for credit assessment';
COMMENT ON TABLE documents IS 'File management for loan application documents';
COMMENT ON TABLE underwriting_decisions IS 'Underwriter decisions and loan terms';
COMMENT ON TABLE workflow_status IS 'Tracks loan application progress through workflow steps';
COMMENT ON TABLE audit_logs IS 'Comprehensive audit trail for compliance and security';
COMMENT ON TABLE system_settings IS 'Configurable system parameters and business rules';

-- Migration completed successfully
SELECT 'Loan Origination Database Schema v1.0 created successfully!' as status;
