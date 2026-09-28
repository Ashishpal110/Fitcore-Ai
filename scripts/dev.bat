@echo off
echo Starting FitCore Development Environment...

start "FitCore Backend" cmd /k "cd ..\backend && (if exist .venv\Scripts\activate.bat (call .venv\Scripts\activate.bat)) && uvicorn app.main:app --reload --port 8000"
start "FitCore Frontend" cmd /k "cd ..\frontend && npm run dev"

echo Development servers launched!
echo Backend:  http://localhost:8000
echo Swagger:  http://localhost:8000/docs
echo Frontend: http://localhost:5173
