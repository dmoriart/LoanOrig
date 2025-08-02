# Database Schema Documentation
## Loan Origination System

### Overview
This document describes the comprehensive PostgreSQL database schema for the Loan Origination System. The schema is designed to handle the complete loan application lifecycle from initial application through underwriting, approval, and compliance tracking.

### Database Design Principles
- **Compliance First**: Designed with audit trails and regulatory compliance in mind
- **Scalability**: Uses UUIDs for primary keys to support distributed systems
- **Data Integrity**: Comprehensive constraints and foreign key relationships
- **Performance**: Strategic indexes for common query patterns
- **Security**: Role-based access control and sensitive data handling

---

## Tables Overview

### Core Business Tables

#### 1. Users Table
**Purpose**: Stores all system users including applicants, underwriters, processors, and administrators.

**Key Fields**:
- `id` (UUID): Primary key
- `email` (VARCHAR): Unique identifier for login
- `role` (ENUM): User role (applicant, underwriter, admin, processor, manager)
- `password_hash` (VARCHAR): Bcrypt hashed password
- `is_active` (BOOLEAN): Account status
- `email_verified` (BOOLEAN): Email verification status

**Relationships**:
- One-to-many with loan_applications (as applicant)
- One-to-many with loan_applications (as assigned underwriter)
- One-to-many with documents (as uploader)
- One-to-many with underwriting_decisions

#### 2. Loan Applications Table
**Purpose**: Main table storing loan application data and personal information.

**Key Fields**:
- `id` (UUID): Primary key
- `loan_number` (VARCHAR): Human-readable unique identifier
- `loan_amount` (DECIMAL): Requested loan amount
- `property_value` (DECIMAL): Property valuation
- `credit_score` (INTEGER): Applicant's credit score
- `status` (ENUM): Application status
- `assigned_underwriter_id` (UUID): Current underwriter

**Status Flow**:
```
draft → submitted → under_review → approved/rejected → funded → closed
```

### Financial Data Tables

#### 3. Applicant Income Table
**Purpose**: Detailed income tracking for debt-to-income calculations.

**Income Types**:
- Salary, Hourly, Commission, Bonus
- Self-employment, Rental, Investment income

#### 4. Applicant Assets Table
**Purpose**: Asset verification and down payment validation.

**Asset Types**:
- Bank accounts (checking, savings)
- Investment accounts
- Real estate, vehicles
- Retirement accounts

#### 5. Applicant Liabilities Table
**Purpose**: Debt tracking for credit analysis.

**Liability Types**:
- Credit cards, auto loans
- Mortgages, student loans
- Personal loans

### Document Management

#### 6. Documents Table
**Purpose**: File management with verification workflow.

**Key Features**:
- File metadata (size, type, path)
- Verification status and history
- Required document tracking
- Expiration date management

**Document Status Flow**:
```
pending → uploaded → verified/rejected
```

### Underwriting & Workflow

#### 7. Underwriting Decisions Table
**Purpose**: Records underwriter decisions and loan terms.

**Decision Types**:
- Approve, Reject, Conditional Approval
- Pending, Request More Information

**Key Calculations**:
- Debt-to-income ratio
- Loan-to-value ratio
- Risk scoring

#### 8. Workflow Status Table
**Purpose**: Tracks application progress through defined steps.

**Features**:
- Step ordering and completion tracking
- Assignment management
- Due date monitoring
- Progress comments

### Compliance & Auditing

#### 9. Audit Logs Table
**Purpose**: Comprehensive audit trail for regulatory compliance.

**Tracked Information**:
- User actions and data changes
- IP addresses and session tracking
- Before/after values (JSONB)
- Regulatory references (TRID, HMDA, etc.)

#### 10. System Settings Table
**Purpose**: Configurable business rules and parameters.

**Examples**:
- Maximum loan amounts
- Minimum credit scores
- DTI ratio limits
- Document retention periods

---

## Key Relationships

### Primary Relationships
```
Users (1) ←→ (M) Loan Applications
Loan Applications (1) ←→ (M) Income Records
Loan Applications (1) ←→ (M) Assets
Loan Applications (1) ←→ (M) Liabilities
Loan Applications (1) ←→ (M) Documents
Loan Applications (1) ←→ (M) Underwriting Decisions
```

### Secondary Relationships
```
Users (1) ←→ (M) Documents (uploader)
Users (1) ←→ (M) Documents (verifier)
Users (1) ←→ (M) Underwriting Decisions
Users (1) ←→ (M) Workflow Status (assignee)
```

---

## Indexes & Performance

### Primary Indexes
- **Users**: email, role, is_active
- **Loan Applications**: applicant_id, status, loan_number, submitted_at
- **Documents**: application_id, status, document_type
- **Audit Logs**: user_id, entity_type/entity_id, created_at

### Composite Indexes
- **Financial Data**: All tables indexed on application_id
- **Workflow**: application_id + status
- **Audit**: entity_type + entity_id for fast lookups

---

## Business Rules & Constraints

### Data Validation
- Credit scores: 300-850 range
- Loan amounts: Must be positive
- DTI calculations: Automated via stored functions
- Email uniqueness: Enforced at database level

### Referential Integrity
- Cascade deletes for child records
- Foreign key constraints on all relationships
- UUID consistency across all tables

### Audit Requirements
- All data changes logged
- User session tracking
- IP address recording
- Regulatory compliance notes

---

## Security Features

### Access Control
- Role-based permissions in application layer
- Sensitive field identification
- Password hashing (bcrypt)
- Session management

### Data Protection
- PII encryption recommendations
- Audit trail immutability
- Document retention policies
- Compliance reporting capabilities

---

## Migration Strategy

### Initial Setup
1. Run `001_initial_schema.sql` migration
2. Execute database utility: `python db_utils.py init`
3. Create seed data with test users
4. Configure application environment variables

### Future Migrations
- Use Alembic for schema changes
- Maintain backward compatibility
- Test migrations on staging environment
- Document all changes in migration files

---

## Monitoring & Maintenance

### Key Metrics
- Application processing times
- Document verification rates
- Underwriter workload distribution
- System performance indicators

### Regular Tasks
- Audit log archival
- Document cleanup (retention policy)
- Performance optimization
- Backup verification

---

## Sample Queries

### Common Business Queries

```sql
-- Get applications by status
SELECT la.*, u.first_name, u.last_name 
FROM loan_applications la
JOIN users u ON la.applicant_id = u.id
WHERE la.status = 'under_review';

-- Calculate DTI ratio
SELECT application_id, calculate_dti_ratio(application_id) as dti_ratio
FROM loan_applications
WHERE status = 'submitted';

-- Underwriter workload
SELECT u.first_name, u.last_name, COUNT(la.id) as active_loans
FROM users u
LEFT JOIN loan_applications la ON u.id = la.assigned_underwriter_id
WHERE u.role = 'underwriter' AND la.status IN ('under_review', 'submitted')
GROUP BY u.id, u.first_name, u.last_name;

-- Document status summary
SELECT document_type, status, COUNT(*) as count
FROM documents
GROUP BY document_type, status
ORDER BY document_type, status;
```

### Compliance Queries

```sql
-- Recent audit activity
SELECT user_email, action, entity_type, created_at
FROM audit_logs
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;

-- Applications missing required documents
SELECT la.loan_number, la.applicant_id, COUNT(d.id) as document_count
FROM loan_applications la
LEFT JOIN documents d ON la.id = d.application_id AND d.is_required = true
WHERE la.status != 'draft'
GROUP BY la.id, la.loan_number, la.applicant_id
HAVING COUNT(d.id) < 5; -- Assuming 5 required documents
```

This schema provides a robust foundation for a production loan origination system with comprehensive compliance, audit, and workflow management capabilities.
