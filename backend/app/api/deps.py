import uuid
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

# HTTPBearer security scheme for Swagger UI and Authorization header parsing
security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    auth_header: Annotated[HTTPAuthorizationCredentials | None, Depends(security_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Dependency that extracts and validates the JWT Bearer token and returns the current user."""
    if not auth_header or not auth_header.credentials:
        raise UnauthorizedException("Authentication token is missing")

    token = auth_header.credentials
    payload = decode_access_token(token)

    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedException("Invalid token payload: subject missing")

    try:
        user_id = uuid.UUID(sub)
    except (ValueError, TypeError):
        raise UnauthorizedException("Invalid user identifier in token")

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise UnauthorizedException("User associated with token not found")

    if not user.is_active:
        raise UnauthorizedException("User account is inactive")

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Dependency verifying the user is active."""
    if not current_user.is_active:
        raise UnauthorizedException("User account is inactive")
    return current_user
