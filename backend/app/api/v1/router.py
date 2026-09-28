from fastapi import APIRouter
from app.api.v1.endpoints import auth, health

api_router = APIRouter()

# Core System & Health Endpoints
api_router.include_router(health.router, tags=["System Health"])

# Authentication Endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Note: Future endpoint modules will be mounted here in subsequent phases:
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
# api_router.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
# api_router.include_router(routines.router, prefix="/routines", tags=["Routines"])
# api_router.include_router(progress.router, prefix="/progress", tags=["Progress Analytics"])
# api_router.include_router(body.router, prefix="/body", tags=["Body Measurements"])
