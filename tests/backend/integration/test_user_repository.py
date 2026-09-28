import uuid
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_user_repository_create_and_get(db_session: AsyncSession):
    """Verify creating and fetching a user via UserRepository."""
    repo = UserRepository(db_session)

    new_user = User(
        name="John Doe",
        email="john.doe@example.com",
        password_hash="fakehash123",
        is_active=True,
    )

    created = await repo.create(new_user)
    await db_session.commit()

    assert created.id is not None
    assert isinstance(created.id, uuid.UUID)
    assert created.email == "john.doe@example.com"
    assert created.created_at is not None

    # Fetch by ID
    fetched_by_id = await repo.get_by_id(created.id)
    assert fetched_by_id is not None
    assert fetched_by_id.name == "John Doe"

    # Fetch by Email
    fetched_by_email = await repo.get_by_email("JOHN.DOE@EXAMPLE.COM")
    assert fetched_by_email is not None
    assert fetched_by_email.id == created.id


@pytest.mark.asyncio
async def test_user_repository_duplicate_email_rejected(db_session: AsyncSession):
    """Verify that inserting a duplicate email raises IntegrityError."""
    repo = UserRepository(db_session)

    user1 = User(
        name="User 1",
        email="duplicate@example.com",
        password_hash="hash1",
    )
    await repo.create(user1)
    await db_session.commit()

    user2 = User(
        name="User 2",
        email="duplicate@example.com",
        password_hash="hash2",
    )
    with pytest.raises(IntegrityError):
        await repo.create(user2)
        await db_session.commit()
    await db_session.rollback()
