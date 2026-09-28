import pytest
from httpx import AsyncClient
from datetime import timedelta
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient):
    """Verify successful user registration returns 201 with access token and user profile."""
    payload = {
        "name": "Ashish",
        "email": "ashish@example.com",
        "password": "securepassword123",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0
    assert "user" in data

    user = data["user"]
    assert user["name"] == "Ashish"
    assert user["email"] == "ashish@example.com"
    assert user["is_active"] is True
    assert "id" in user
    assert "created_at" in user
    # Ensure security sensitive fields are not exposed
    assert "password" not in user
    assert "password_hash" not in user
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    """Verify registering an existing email returns 409 Conflict."""
    payload = {
        "name": "First User",
        "email": "duplicate@example.com",
        "password": "securepassword123",
    }
    # First registration
    resp1 = await async_client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    # Second registration with same email (different casing / whitespace)
    dup_payload = {
        "name": "Second User",
        "email": "  DUPLICATE@example.COM ",
        "password": "anotherpassword123",
    }
    resp2 = await async_client.post("/api/v1/auth/register", json=dup_payload)
    assert resp2.status_code == 409
    data = resp2.json()
    assert "error" in data
    assert "already exists" in data["error"]["message"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email(async_client: AsyncClient):
    """Verify registering with an invalid email returns 422 Unprocessable Entity."""
    payload = {
        "name": "Invalid Email",
        "email": "not-an-email",
        "password": "securepassword123",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_register_short_password(async_client: AsyncClient):
    """Verify registering with password < 8 chars returns 422 Unprocessable Entity."""
    payload = {
        "name": "Short Pass",
        "email": "short@example.com",
        "password": "12345",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_register_missing_fields(async_client: AsyncClient):
    """Verify registering with missing required fields returns 422."""
    response = await async_client.post("/api/v1/auth/register", json={"name": "Incomplete"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    """Verify login with correct credentials returns 200 OK and access token."""
    # Register first
    await async_client.post(
        "/api/v1/auth/register",
        json={"name": "Login User", "email": "login@example.com", "password": "mypassword123"},
    )

    # Login
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "LOGIN@example.com", "password": "mypassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_incorrect_password(async_client: AsyncClient):
    """Verify login with wrong password returns 401 with generic error."""
    await async_client.post(
        "/api/v1/auth/register",
        json={"name": "User", "email": "wrongpass@example.com", "password": "correctpassword123"},
    )

    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpass@example.com", "password": "incorrectpassword123"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "invalid email or password" in data["error"]["message"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client: AsyncClient):
    """Verify login with nonexistent user returns 401 with same generic error."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "ghost@example.com", "password": "somepassword123"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "invalid email or password" in data["error"]["message"].lower()


@pytest.mark.asyncio
async def test_login_malformed_request(async_client: AsyncClient):
    """Verify login with invalid format returns 422."""
    response = await async_client.post("/api/v1/auth/login", json={"email": "not-an-email"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_current_user_me_success(async_client: AsyncClient):
    """Verify GET /api/v1/auth/me returns user profile with valid Bearer token."""
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={"name": "Me User", "email": "me@example.com", "password": "mypassword123"},
    )
    token = reg_resp.json()["access_token"]

    response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Me User"
    assert data["email"] == "me@example.com"
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_get_current_user_me_missing_token(async_client: AsyncClient):
    """Verify GET /api/v1/auth/me without token returns 401 Unauthorized."""
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_get_current_user_me_invalid_token(async_client: AsyncClient):
    """Verify GET /api/v1/auth/me with invalid token returns 401 Unauthorized."""
    response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_get_current_user_me_expired_token(async_client: AsyncClient):
    """Verify GET /api/v1/auth/me with expired token returns 401 Unauthorized."""
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={"name": "Expire User", "email": "expire@example.com", "password": "mypassword123"},
    )
    user_id = reg_resp.json()["user"]["id"]
    expired_token = create_access_token(subject=user_id, expires_delta=timedelta(seconds=-60))

    response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "expired" in data["error"]["message"].lower()
