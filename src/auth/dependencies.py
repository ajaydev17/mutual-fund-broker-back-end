from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from fastapi import status, Request, Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService
from typing import List, Any
from src.errors import InvalidToken, RefreshTokenRequired, AccessTokenRequired

# create an instance of the user service
user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please Override this method in child classes")


# created a class for raising access token is not provided
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()


# created a class for raising when refresh toke is not provided
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()