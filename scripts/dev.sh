#!/bin/bash
echo "Starting FitCore Development Environment..."

# Start backend
(
  cd ../backend || exit
  if [ -d ".venv" ]; then
    source .venv/bin/activate
  fi
  uvicorn app.main:app --reload --port 8000
) &

# Start frontend
(
  cd ../frontend || exit
  npm run dev
) &

echo "Development servers running in background."
echo "Backend:  http://localhost:8000"
echo "Swagger:  http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"

wait
