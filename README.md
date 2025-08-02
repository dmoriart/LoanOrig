# Loan Origination System

A full-stack loan origination system built with React frontend, Python backend (Flask + FastAPI), and PostgreSQL database.

## Architecture

- **Frontend**: React + Vite + Tailwind CSS (deployed on Netlify)
- **Backend**: Python with Flask and FastAPI (deployed on Render)
- **Database**: PostgreSQL (hosted on Supabase)

## Project Structure

```
LoanOrig/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── LoanApplication.jsx
│   │   │   └── LoanList.jsx
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # App entry point
│   ├── package.json         # Frontend dependencies
│   └── netlify.toml         # Netlify deployment config
├── backend/                 # Python backend services
│   ├── flask_app.py         # Flask API server
│   ├── fastapi_app.py       # FastAPI server
│   ├── database.py          # Database models and setup
│   ├── requirements.txt     # Python dependencies
│   ├── render.yaml          # Render deployment config
│   └── .env.example         # Environment variables template
└── .github/
    └── copilot-instructions.md
```

## Features

### Frontend Features
- Loan application form with validation
- Loan dashboard showing all applications
- Responsive design with Tailwind CSS
- Real-time status updates
- Clean, modern UI

### Backend Features
- Dual API architecture (Flask + FastAPI)
- RESTful endpoints for loan operations
- Data validation with Pydantic
- PostgreSQL integration
- Environment-based configuration
- CORS support for cross-origin requests

### Database Features
- Loan applications storage
- User management
- SQLAlchemy ORM
- Database migrations with Alembic

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL database (Supabase account recommended)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your database credentials and other configuration.

6. Run the Flask server:
   ```bash
   python flask_app.py
   ```
   Available at `http://localhost:5000`

7. Or run the FastAPI server:
   ```bash
   python fastapi_app.py
   ```
   Available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

## API Endpoints

### Flask API (Port 5000)
- `GET /health` - Health check
- `GET /api/loans` - Get all loan applications
- `POST /api/loans` - Create a new loan application

### FastAPI API (Port 8000)
- `GET /health` - Health check
- `GET /api/v1/loans` - Get all loan applications
- `POST /api/v1/loans` - Create a new loan application
- `GET /api/v1/loans/{loan_id}` - Get a specific loan application
- `GET /docs` - Interactive API documentation

## Database Setup

### Using Supabase

1. Create a new project on [Supabase](https://supabase.com)
2. Get your database URL from the project settings
3. Update the `DATABASE_URL` in your `.env` file
4. Run the database setup script:
   ```bash
   python database.py
   ```

### Local PostgreSQL

1. Install PostgreSQL locally
2. Create a database named `loan_origination`
3. Update the `DATABASE_URL` in your `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/loan_origination
   ```

## Deployment

### Frontend (Netlify)

1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Deploy automatically on push to main branch

### Backend (Render)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the `render.yaml` configuration
4. Set environment variables in Render dashboard
5. Deploy automatically on push to main branch

## Environment Variables

### Frontend
No environment variables required for basic setup.

### Backend
Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FASTAPI_ENV=development
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
PORT=8000
FRONTEND_URL=https://your-app.netlify.app
```

## Development

### Running Tests
```bash
cd backend
python -m pytest
```

### Database Migrations
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
