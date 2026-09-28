from datetime import timedelta
import pytest
from app.core.exceptions import UnauthorizedException
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing_and_verification():
    """Verify that password hashing creates secure hashes and verifies matching passwords."""
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False


def test_jwt_token_creation_and_decoding():
    """Verify that JWT tokens encode the user subject and decode correctly."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    token = create_access_token(subject=user_id)

    payload = decode_access_token(token)
    assert payload["sub"] == user_id
    assert "exp" in payload
    assert "iat" in payload


def test_jwt_token_expired():
    """Verify that expired JWT tokens raise UnauthorizedException."""
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    # Token expired 1 minute ago
    token = create_access_token(subject=user_id, expires_delta=timedelta(seconds=-60))

    with pytest.raises(UnauthorizedException) as exc_info:
        decode_access_token(token)
    assert "expired" in str(exc_info.value.message).lower()


def test_jwt_token_invalid():
    """Verify that malformed or forged JWT tokens raise UnauthorizedException."""
    with pytest.raises(UnauthorizedException) as exc_info:
        decode_access_token("not.a.valid.jwt.token")
    assert "invalid" in str(exc_info.value.message).lower()
