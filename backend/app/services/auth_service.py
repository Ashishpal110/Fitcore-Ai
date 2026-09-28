import uuid
from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, NotFoundException, UnauthorizedException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate


class AuthService:
    """Service handling user registration, authentication, and token issuance."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, user_in: UserCreate) -> Tuple[User, str, int]:
        """Register a new user, ensure email uniqueness, hash password, and issue access token."""
        normalized_email = user_in.email.strip().lower()

        existing_user = await self.user_repo.get_by_email(normalized_email)
        if existing_user:
            raise ConflictException(
                message="An account with this email address already exists",
                details={"email": normalized_email},
            )

        # Hash password securely
        password_hash = get_password_hash(user_in.password)

        new_user = User(
            name=user_in.name,
            email=normalized_email,
            password_hash=password_hash,
            is_active=True,
        )

        created_user = await self.user_repo.create(new_user)
        await self.session.commit()

        # Generate JWT access token
        access_token = create_access_token(subject=str(created_user.id))
        expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60

        return created_user, access_token, expires_in

    async def authenticate(self, login_data: LoginRequest) -> Tuple[User, str, int]:
        """Authenticate user credentials and issue an access token."""
        normalized_email = login_data.email.strip().lower()

        user = await self.user_repo.get_by_email(normalized_email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise UnauthorizedException(message="Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException(message="Account is inactive")

        access_token = create_access_token(subject=str(user.id))
        expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60

        return user, access_token, expires_in

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        """Retrieve user by ID or raise NotFoundException."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(resource="User", identifier=user_id)
        return user
