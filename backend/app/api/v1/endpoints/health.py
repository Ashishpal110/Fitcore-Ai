from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

router = APIRouter()


@router.get(
    "/health",
    summary="Service & Database Health Check",
    description="Check the operational status of the FitCore API and PostgreSQL database connection.",
    response_model=Dict[str, Any],
)
async def get_health_status(
    response: Response,
    session: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    db_status = "connected"
    overall_status = "healthy"

    try:
        # Execute quick heartbeat query against database
        await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"
        overall_status = "degraded"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": overall_status,
        "database": db_status,
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0-phase1",
    }
