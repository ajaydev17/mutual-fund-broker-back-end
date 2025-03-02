from src.db.models import User
from sqlmodel import select

access_token = None

# Helper function to create a test user
async def create_test_user(client, db_session_integration):
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    headers = {"Content-Type": "application/json"}
    response = await client.post("api/v1/auth/signup", json=user_data, headers=headers)

    # Ensure user is created successfully
    assert response.status_code == 201

    # Fetch the user from the database
    statement = select(User).where(User.email == user_data['email'])
    result = await db_session_integration.exec(statement)
    user = result.first()

    assert user is not None  # Ensure user is not None

    # Mark user as verified
    user.is_verified = True
    db_session_integration.add(user)
    await db_session_integration.commit()
    await db_session_integration.refresh(user)

    return user


# Test case for creating a user
async def test_integrate_create_user(client, db_session_integration):
    user = await create_test_user(client, db_session_integration)

    # Verify user data
    assert user.email == "testuser@example.com"
    return user


# Test case for user login
async def test_integrate_user_login(client, db_session_integration):
    # User login data
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    # Attempt to log in
    headers = {"Content-Type": "application/json"}
    response = await client.post("api/v1/auth/login", json=user_data, headers=headers)

    # Debug print to check the login response
    print("Login Response Status:", response.status_code)
    print("Login Response Body:", response.json())

    # Verify login response
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Store the token globally
    global access_token
    access_token = response.json().get("access_token")

    return response


async def test_integrate_get_current_user_info(client, db_session_integration):
    global access_token  # Access the global token

    # Ensure the token is available
    assert access_token is not None, "Access token is not set. Login might have failed."

    # Make a request to get current user info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("api/v1/auth/me", headers=headers)

    # Verify response
    assert response.status_code == 200
    user_info = response.json()
    assert user_info["email"] == "testuser@example.com"
    assert user_info["is_verified"] is True

    print("Current User Info:", user_info)
    return user_info

async def test_integrate_create_investment(client, db_session_integration):
    global access_token  # Access the global token

    # Investment data
    investment_data = {
        "scheme_code": 100044,
        "units": 10,
        "fund_family": "Aditya Birla Sun Life Mutual Fund",
        "scheme_name": "Aditya Birla Sun Life Liquid Fund - Retail - IDCW",
        "nav": 163.694,
        "date": "24-Feb-2025",
        "current_value": 1636.94
    }

    # Send a POST request to create investment
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("api/v1/investment", json=investment_data, headers=headers)

    print(response.json())

    # Verify the response
    assert response.status_code == 201
    investment = response.json()
    assert investment["scheme_code"] == investment_data["scheme_code"]
    assert investment["current_value"] == investment_data["current_value"]

    print("Investment Created:", investment)
    return investment


async def test_integrate_update_investment(client, db_session_integration):
    global access_token

    investment_update_data = {
        'scheme_code': 100044,
        'units': 20,
        'current_value': 3273.88
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.patch(f"api/v1/investment", json=investment_update_data, headers=headers)

    assert response.status_code == 200
    investment = response.json()
    assert investment["units"] == investment_update_data["units"]
    assert investment["current_value"] == investment_update_data["current_value"]

    print("Investment Updated:", investment)


async def test_integrate_get_investment(client, db_session_integration):
    global access_token
    scheme_code = 100044


    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"api/v1/investment/get-an-investment/{scheme_code}", headers=headers)

    assert response.status_code == 200
    investment = response.json()
    assert investment["scheme_code"] == scheme_code

    print("Retrieved Investment:", investment)


async def test_integrate_delete_investment(client, db_session_integration):
    global access_token
    scheme_code = 100044

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.delete(f"api/v1/investment/delete-an-investment/{scheme_code}", headers=headers)

    assert response.status_code == 204

    print("Investment Deleted:", scheme_code)


async def test_integrate_integrate_user_logout(client, db_session_integration):
    global access_token  # Access the global variable

    # Ensure the token is available
    if not access_token:
        await test_integrate_user_login(client, db_session_integration)

    # Use the token to log out
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("api/v1/auth/logout", headers=headers)

    # Verify logout response
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful!!."
