#!/bin/bash

# Loan Origination System Startup Script

echo "🏦 Loan Origination System Setup"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📋 Pre-flight checks:"

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js $(node --version) is installed"
else
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python $(python3 --version) is installed"
else
    echo "❌ Python is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Start frontend in background
echo "📱 Starting Frontend (React + Vite)..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment
sleep 2

# Start FastAPI in background
echo "⚡ Starting FastAPI Server..."
cd backend && ../../../.venv/bin/python fastapi_app.py &
FASTAPI_PID=$!
cd ..

echo ""
echo "🎉 Services are starting up!"
echo ""
echo "📊 Access your application:"
echo "  Frontend:    http://localhost:5173"
echo "  FastAPI:     http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo ""
echo "⚠️  Note: Make sure to configure your database connection in backend/.env"
echo ""
echo "🛑 To stop all services, press Ctrl+C"

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $FRONTEND_PID $FASTAPI_PID 2>/dev/null; exit" INT
wait
