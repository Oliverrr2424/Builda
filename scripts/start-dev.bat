@echo off
echo Starting the Builda development environment...

echo Starting backend service...
cd backend
start "Backend" cmd /k "python main.py"

echo Waiting for backend to boot...
timeout /t 3 /nobreak > nul

echo Starting frontend service...
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo Development environment is ready!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API docs: http://localhost:8000/docs

pause
