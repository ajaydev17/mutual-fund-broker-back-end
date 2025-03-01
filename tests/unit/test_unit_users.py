import pytest
from pydantic import ValidationError
from src.db.models import User
from src.auth.schemas import UserCreateSchema, UserInvestmentSchemaView
from tests.factories.models_factory import MockUser
from faker import Faker
from unittest.mock import AsyncMock
from passlib.hash import bcrypt
from src.config import config_obj
from datetime import datetime, timedelta
import jwt

faker = Faker()


"""
- [ ] Test users schema valid and invalid data 
"""


async def test_unit_schema_users_validation():
    valid_data = {
        "email": "devadigaajay1729@gmail.com",
        "password": "test1234"
    }

    category = User(**valid_data)
    assert category.email == 'devadigaajay1729@gmail.com'
    assert category.is_verified is False

    invalid_data = {
        "email": "devadigaajay1729@gmail.com",
    }

    with pytest.raises(ValidationError):
        UserCreateSchema(**invalid_data)


"""
- [ ] Sign Up related tests
"""

@pytest.mark.asyncio
async def test_signup_success(client, mock_session, monkeypatch):
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=None))

    monkeypatch.setattr("src.auth.services.UserService.create_user", AsyncMock(return_value={"email": user_data["email"], "user_id": "1234"}))

    response = await client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 201
    assert "user" in response.json()
    assert response.json()["user"]["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_signup_existing_user(client, mock_session, monkeypatch):
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    # Mock get_user_by_email to return an existing user
    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value={"email": user_data["email"]}))

    response = await client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 403
    assert response.json()["message"] == "User with email already exists!!."


"""
- [ ] login related tests
"""

@pytest.mark.asyncio
async def test_login_success(client, monkeypatch):
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    hashed_password = bcrypt.hash(user_data["password"])


    mock_user = MockUser(
        email=user_data["email"],
        password_hash=hashed_password,
        is_verified=True
    )

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=mock_user))

    monkeypatch.setattr("src.auth.utils.verify_password_hash", AsyncMock(return_value=True))

    response = await client.post("/api/v1/auth/login", json=user_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, monkeypatch):
    user_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=None))

    response = await client.post("/api/v1/auth/login", json=user_data)

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid credentials!!."



"""
- [ ] logout related tests
"""


@pytest.mark.asyncio
async def test_logout_success(client, monkeypatch):

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.auth.dependencies.check_jti_in_blocklist", AsyncMock(return_value=False))

    monkeypatch.setattr("src.auth.routes.add_jti_to_blocklist", AsyncMock())

    response = await client.post("/api/v1/auth/logout", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful!!."


@pytest.mark.asyncio
async def test_logout_without_token(client):
    response = await client.post("/api/v1/auth/logout")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

"""
- [ ] Get Current User related tests
"""

@pytest.mark.asyncio
async def test_get_current_user(client, monkeypatch):

    # Sample user payload
    mock_user_investments = {
        "email": "testuser@example.com",
        "user_id": "d3f865a9-2e1c-45cb-8130-05462f562e69",
        "password_hash" :bcrypt.hash('securepassword'),
        "is_verified": True,
        "created_at" :faker.date_time(),
        "updated_at" :faker.date_time(),
        "investments": []
    }

    fake_payload = {
        "user": {"email": "testuser@example.com", "user_id": "d3f865a9-2e1c-45cb-8130-05462f562e69"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.auth.dependencies.get_current_user", AsyncMock(return_value=mock_user_investments))

    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == mock_user_investments["email"]
    assert response.json()["user_id"] == mock_user_investments["user_id"]


@pytest.mark.asyncio
async def test_get_current_user_no_token(client):
    """Test case when no token is provided Should return 403 Unauthorized."""

    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"









