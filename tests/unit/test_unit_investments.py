import pytest
from pydantic import ValidationError
from src.db.models import Investment
from src.investment.schemas import InvestmentCreateSchema
from tests.factories.models_factory import MockInvestment, MockInvestmentUpdate, MockInvestmentDelete, MockInvestmentFetch
from faker import Faker
from unittest.mock import AsyncMock
from src.config import config_obj
from datetime import datetime, timedelta
import jwt

faker = Faker()


"""
- [ ] Test investment schema valid and invalid data
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

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    monkeypatch.setattr("src.investment.services.InvestmentService.create_an_investment", AsyncMock(return_value=mock_investment_dict))

    response = await client.post("/api/v1/investment", headers=headers, json=mock_investment_dict)

    assert response.status_code == 201
    assert "scheme_code" in response.json()
    assert response.json()["scheme_code"]== mock_investment_dict["scheme_code"]


@pytest.mark.asyncio
async def test_create_investment_already_exists(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {"Authorization": f"Bearer {fake_token}"}

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))

    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment_dict))

    response = await client.post("/api/v1/investment", headers=headers, json=mock_investment_dict)

    assert response.status_code == 403
    assert response.json()["message"]== "Investment already exists for this scheme code!!."


async def test_create_investment_invalid_token(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.post("/api/v1/investment", json=mock_investment_dict)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


"""
- [ ] Update Investment related tests
"""

@pytest.mark.asyncio
async def test_update_investment_success(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    mock_investment_update = MockInvestmentUpdate(
        scheme_code=100044,
        units=20,
        current_value=3273.88
    )

    mock_investment_update_dict = mock_investment_update.__dict__

    mock_investment_updated = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=20,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=3273.88
    )

    mock_investment_updated_dict = mock_investment_updated.__dict__

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment_dict))
    monkeypatch.setattr("src.investment.services.InvestmentService.update_an_investment", AsyncMock(return_value=mock_investment_updated_dict))

    response = await client.patch("/api/v1/investment", headers=headers, json=mock_investment_update_dict)


    assert response.status_code == 200
    assert "scheme_code" in response.json()
    assert response.json()["scheme_code"] == mock_investment_update_dict["scheme_code"]
    assert response.json()["units"] == 20
    assert response.json()["current_value"] == 3273.88


@pytest.mark.asyncio
async def test_update_investment_scheme_code_not_exists(client, mock_session, monkeypatch):

    mock_investment_update = MockInvestmentUpdate(
        scheme_code=100044,
        units=20,
        current_value=3273.88
    )

    mock_investment_update_dict = mock_investment_update.__dict__

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.patch("/api/v1/investment", headers=headers, json=mock_investment_update_dict)


    assert response.status_code == 404
    assert response.json()["message"] == "Investment not found!!."


@pytest.mark.asyncio
async def test_update_investment_invalid_token(client, mock_session, monkeypatch):

    mock_investment_update = MockInvestmentUpdate(
        scheme_code=100044,
        units=20,
        current_value=3273.88
    )

    mock_investment_update_dict = mock_investment_update.__dict__

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)


    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.patch("/api/v1/investment", json=mock_investment_update_dict)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


"""
- [ ] Delete Investment related tests
"""

@pytest.mark.asyncio
async def test_delete_investment_success(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    mock_investment_delete = MockInvestmentDelete(
        scheme_code=100044
    )

    mock_investment_delete_dict = mock_investment_delete.__dict__
    scheme_code = mock_investment_delete_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment_dict))
    monkeypatch.setattr("src.investment.services.InvestmentService.delete_an_investment", AsyncMock(return_value=mock_investment_dict))

    response = await client.delete(f"/api/v1/investment/delete-an-investment/{scheme_code}", headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_investment_scheme_code_not_exists(client, mock_session, monkeypatch):

    mock_investment_delete = MockInvestmentDelete(
        scheme_code=100044
    )

    mock_investment_delete_dict = mock_investment_delete.__dict__
    scheme_code = mock_investment_delete_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.delete(f"/api/v1/investment/delete-an-investment/{scheme_code}", headers=headers)

    assert response.status_code == 404
    assert response.json()["message"] == "Investment not found!!."


@pytest.mark.asyncio
async def test_delete_investment_invalid_token(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    mock_investment_delete = MockInvestmentDelete(
        scheme_code=100044
    )

    mock_investment_delete_dict = mock_investment_delete.__dict__
    scheme_code = mock_investment_delete_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment_dict))

    response = await client.delete(f"/api/v1/investment/delete-an-investment/{scheme_code}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


"""
- [ ] Get Investment related tests
"""

@pytest.mark.asyncio
async def test_get_investment_success(client, mock_session, monkeypatch):

    mock_investment = MockInvestment(
        investment_id="d3f865a9-2e1c-45cb-8130-05462f562e73",
        scheme_code=100044,
        units=10,
        fund_family="Aditya Birla Sun Life Mutual Fund",
        scheme_name="Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        nav=163.694,
        date="24-Feb-2025",
        current_value=1636.94
    )

    mock_investment_dict = mock_investment.__dict__

    mock_investment_get = MockInvestmentFetch(
        scheme_code=100044,
    )

    mock_investment_get_dict = mock_investment_get.__dict__
    scheme_code = mock_investment_get_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=mock_investment_dict))

    response = await client.get(f"/api/v1/investment/get-an-investment/{scheme_code}", headers=headers)


    assert response.status_code == 200
    assert "scheme_code" in response.json()
    assert response.json()["scheme_code"] == mock_investment_dict["scheme_code"]
    assert response.json()["units"] == 10
    assert response.json()["current_value"] == 1636.94


@pytest.mark.asyncio
async def test_get_investment_scheme_code_not_exits(client, mock_session, monkeypatch):

    mock_investment_get = MockInvestmentFetch(
        scheme_code=100044,
    )

    mock_investment_get_dict = mock_investment_get.__dict__
    scheme_code = mock_investment_get_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    headers = {
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    }

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.get(f"/api/v1/investment/get-an-investment/{scheme_code}", headers=headers)

    assert response.status_code == 404
    assert response.json()["message"] == "Investment not found!!."


@pytest.mark.asyncio
async def test_get_investment_invalid_token(client, mock_session, monkeypatch):

    mock_investment_get = MockInvestmentFetch(
        scheme_code=100044,
    )

    mock_investment_get_dict = mock_investment_get.__dict__
    scheme_code = mock_investment_get_dict['scheme_code']

    fake_payload = {
        "user": {"email": "test@example.com", "user_id": "12345"},
        "exp": datetime.now() + timedelta(minutes=30),
        "jti": "fake-uid",
        "refresh": False
    }

    fake_token = jwt.encode(fake_payload, config_obj.JWT_SECRET_KEY, algorithm=config_obj.JWT_ALGORITHM)

    monkeypatch.setattr("src.auth.utils.decode_access_token", AsyncMock(return_value=fake_payload))
    monkeypatch.setattr("src.investment.services.InvestmentService.get_investment_by_user_id_scheme_code", AsyncMock(return_value=None))

    response = await client.get(f"/api/v1/investment/get-an-investment/{scheme_code}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"
