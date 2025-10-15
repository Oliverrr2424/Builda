#!/bin/bash

echo "Starting the Builda development environment..."

# Ensure Node.js and Python are available
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js first."
    exit 1
fi

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python not found. Please install Python first."
    exit 1
fi

# Start backend
echo "Starting backend service..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait for backend to boot
echo "Waiting for backend to boot..."
sleep 3

# Start frontend
echo "Starting frontend service..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Development environment is ready!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interruption
wait
