# from src.db.models import User
# from sqlmodel import select
#
# """
# - [ ] Test singup related test
# """
#
#
# async def test_integrate_create_user(client, db_session_integration):
#     user_data = {
#         "email": "testuser@example.com",
#         "password": "securepassword"
#     }
#
#     response = await client.post("api/v1/auth/signup", json=user_data)
#
#     statement = select(User).where(User.email == user_data['email'])
#     result = await db_session_integration.exec(statement)
#     user = result.first()
#
#
#     assert user is not None
#     assert response.status_code == 201
#     assert user.email == user_data['email']
#
#
# """
# - [ ] Test POST new category successfully
# """
#
#
# async def test_integrate_user_login(client, db_session_integration):
#
#     user = await test_integrate_create_user(client, db_session_integration)
#     print(user)
#     user.is_verified = True
#     await db_session_integration.add(user)
#     await db_session_integration.commit()
#     await db_session_integration.refresh(user)
#
#     user_data = {
#         "email": "testuser@example.com",
#         "password": "securepassword"
#     }
#
#     response = await client.post("api/v1/auth/login", json=user_data)
#
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#
#     return response
#
# async def test_integrate_user_logout(client, db_session_integration):
#
#     token = await test_integrate_user_login(client, db_session_integration)
#     headers = {"Authorization": f"Bearer {token['access_token']}"}
#
#     response = await client.post("api/v1/auth/logout", headers=headers)
#
#     assert response.status_code == 200
#     assert response.json()["message"] == "Logout successful!!."
