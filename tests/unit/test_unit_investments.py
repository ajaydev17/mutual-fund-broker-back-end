import pytest
from pydantic import ValidationError
from src.db.models import Investment
from src.investment.schemas import InvestmentCreateSchema
from src.auth.utils import create_access_token, decode_access_token
from tests.factories.models_factory import MockInvestment
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
        "scheme_code": 100044,
        "units": 10,
        "fund_family": "Aditya Birla Sun Life Mutual Fund",
        "scheme_name": "Aditya Birla Sun Life Liquid Fund -Retail - IDCW",
        "nav": 163.694,
        "date": "24-Feb-2025",
        "current_value": 1636.94
}

    category = Investment(**valid_data)
    assert category.scheme_code == 100044
    assert category.units == 10
    assert category.fund_family == "Aditya Birla Sun Life Mutual Fund"


    invalid_data = {
        "scheme_code": 100044
    }

    with pytest.raises(ValidationError):
        InvestmentCreateSchema(**invalid_data)


"""
- [ ] Create Investment related tests
"""

@pytest.mark.asyncio
async def test_create_investment_success(client, mock_session, monkeypatch):
    investment_data = {
        "scheme_code": 100044,
        "units": 10,
        "fund_family": "Aditya Birla Sun Life Mutual Fund",
        "scheme_name": "Aditya Birla Sun Life Liquid Fund -Retail - IDCW",
        "nav": 163.694,
        "date": "24-Feb-2025",
        "current_value": 1636.94
    }

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e69",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment))

    monkeypatch.setattr("src.investment.services.InvestmentService.create_an_investment", AsyncMock(return_value=investment_data))

    response = await client.post("/api/v1/investment", headers=headers, json=investment_data)

    assert response.status_code == 201
    assert "scheme_code" in response.json()
    assert response.json()["scheme_code"]== investment_data["scheme_code"]
