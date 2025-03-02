import pytest
from pydantic import ValidationError
from src.db.models import User
from src.auth.schemas import UserCreateSchema, UserInvestmentSchemaView
from tests.factories.models_factory import MockUser, MockUserPasswordHash, MockUserInvestment, MockUserInvestmentPasswordHash
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

    mock_user = MockUser(
        email="testuser@example.com",
        password="securepassword"
    )

    mock_user_dict = mock_user.__dict__

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=None))

    monkeypatch.setattr("src.auth.services.UserService.create_user", AsyncMock(return_value={"email": mock_user_dict['email'], "user_id": "d3f865a9-2e1c-45cb-8130-05462f562e69"}))

    response = await client.post("/api/v1/auth/signup", json=mock_user_dict)

    assert response.status_code == 201
    assert "user" in response.json()
    assert response.json()["user"]["email"] == mock_user_dict['email']


@pytest.mark.asyncio
async def test_signup_existing_user(client, mock_session, monkeypatch):

    mock_user = MockUser(
        email="testuser@example.com",
        password="securepassword"
    )

    mock_user_dict = mock_user.__dict__

    # Mock get_user_by_email to return an existing user
    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value={"email": mock_user_dict['email']}))

    response = await client.post("/api/v1/auth/signup", json=mock_user_dict)

    assert response.status_code == 403
    assert response.json()["message"] == "User with email already exists!!."


"""
- [ ] login related tests
"""

@pytest.mark.asyncio
async def test_login_success(client, monkeypatch):
    mock_user = MockUser(
        email="testuser@example.com",
        password="securepassword"
    )

    hashed_password = bcrypt.hash(mock_user.password)

    mock_user_password = MockUserPasswordHash(
        email=mock_user.email,
        user_id="d3f865a9-2e1c-45cb-8130-05462f562e69",
        password_hash=hashed_password,
        is_verified=True
    )

    mock_user_dict = mock_user.__dict__

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=mock_user_password))

    monkeypatch.setattr("src.auth.utils.verify_password_hash", AsyncMock(return_value=True))

    response = await client.post("/api/v1/auth/login", json=mock_user_dict)

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, monkeypatch):
    mock_user = MockUser(
        email="testuser@example.com",
        password="securepassword"
    )

    mock_user_dict = mock_user.__dict__

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=None))

    response = await client.post("/api/v1/auth/login", json=mock_user_dict)

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
    mock_user = MockUser(
        email="testuser@example.com",
        password="securepassword"
    )

    hashed_password = bcrypt.hash(mock_user.password)

    # Sample user payload
    mock_user_investments_password = MockUserInvestmentPasswordHash(
        user_id="d3f865a9-2e1c-45cb-8130-05462f562e69",
        is_verified=True,
        email = "testuser@example.com",
        investments=None,
        created_at=faker.date_time(),
        updated_at=faker.date_time(),
        password_hash=hashed_password,
    )

    mock_user_investments = MockUserInvestment(
        user_id="d3f865a9-2e1c-45cb-8130-05462f562e69",
        is_verified=True,
        email="testuser@example.com",
        investments=None,
        created_at=faker.date_time(),
        updated_at=faker.date_time(),
    )


    fake_payload = {
        "user": {"email": "testuser@example.com", "user_id": "d3f865a9-2e1c-45cb-8130-05462f562e69"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    hashed_password = bcrypt.hash(mock_user.password)

    mock_user = MockUserPasswordHash(
        email=mock_user.email,
        user_id="d3f865a9-2e1c-45cb-8130-05462f562e69",
        password_hash=hashed_password,
        is_verified=True
    )

    monkeypatch.setattr("src.auth.services.UserService.get_user_by_email", AsyncMock(return_value=mock_user_investments_password))

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.auth.dependencies.get_current_user", AsyncMock(return_value=mock_user_investments))

    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == mock_user_investments.email
    assert response.json()["user_id"] == mock_user_investments.user_id


@pytest.mark.asyncio
async def test_get_current_user_no_token(client):
    """Test case when no token is provided Should return 403 Unauthorized."""

    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"









