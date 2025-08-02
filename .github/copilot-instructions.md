<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Loan Origination System

This is a full-stack loan origination system with the following architecture:

## Frontend (JavaScript/React)
- Built with Vite and React
- Uses Tailwind CSS for styling
- Deployed on Netlify
- Main components: LoanApplication, LoanList
- API integration with backend services

## Backend (Python)
- Dual API approach: Flask and FastAPI
- Flask app: Simple REST API for basic operations
- FastAPI app: Advanced API with automatic documentation and validation
- Deployed on Render
- Database integration with PostgreSQL via SQLAlchemy

## Database
- PostgreSQL hosted on Supabase
- SQLAlchemy ORM for database operations
- Models: LoanApplication, User
- Migration support with Alembic

## Development Guidelines

1. **Frontend Development:**
   - Use functional components with hooks
   - Follow React best practices
   - Use Tailwind CSS classes for styling
   - Handle loading states and errors gracefully
   - Make API calls to either Flask or FastAPI endpoints

2. **Backend Development:**
   - Use type hints for all Python functions
   - Validate input data with Pydantic models (FastAPI) or manual validation (Flask)
   - Include proper error handling and status codes
   - Use environment variables for configuration
   - Follow REST API conventions

3. **Database Operations:**
   - Use SQLAlchemy models for all database operations
   - Create migrations for schema changes
   - Use connection pooling for performance
   - Validate data before database operations

4. **Deployment:**
   - Frontend: Build with `npm run build` and deploy to Netlify
   - Backend: Use gunicorn with uvicorn workers for FastAPI deployment on Render
   - Configure environment variables properly for production

## API Endpoints

### Flask API (Port 5000)
- GET /health - Health check
- GET /api/loans - Get all loans
- POST /api/loans - Create new loan application

### FastAPI API (Port 8000)
- GET /health - Health check
- GET /api/v1/loans - Get all loans with full validation
- POST /api/v1/loans - Create new loan application with validation
- GET /api/v1/loans/{loan_id} - Get specific loan by ID
- Automatic API documentation at /docs

When working on this project, consider the dual-API architecture and choose the appropriate endpoint based on the complexity of the operation needed.
