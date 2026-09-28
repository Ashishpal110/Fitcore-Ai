import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest


def test_user_create_email_normalization():
    """Verify that email addresses are trimmed and lowercased automatically."""
    user = UserCreate(
        name="  Alex Mercer  ",
        email="  Alex.Mercer@Example.COM  ",
        password="ValidPassword123",
    )
    assert user.name == "Alex Mercer"
    assert user.email == "alex.mercer@example.com"


def test_user_create_short_password_rejected():
    """Verify that passwords shorter than 8 characters fail validation."""
    with pytest.raises(ValidationError):
        UserCreate(
            name="Alex",
            email="alex@example.com",
            password="short",
        )


def test_user_create_invalid_email_rejected():
    """Verify that invalid email formats fail validation."""
    with pytest.raises(ValidationError):
        UserCreate(
            name="Alex",
            email="not-an-email",
            password="ValidPassword123",
        )


def test_user_create_empty_name_rejected():
    """Verify that empty or whitespace-only names fail validation."""
    with pytest.raises(ValidationError):
        UserCreate(
            name="   ",
            email="alex@example.com",
            password="ValidPassword123",
        )


def test_login_request_normalization():
    """Verify that login emails are normalized."""
    login = LoginRequest(
        email="  USER@Domain.Org ",
        password="SecretPassword123",
    )
    assert login.email == "user@domain.org"
