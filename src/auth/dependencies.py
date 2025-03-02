from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from fastapi import Request, Depends
from src.auth.services import UserService
from src.errors import InvalidToken, RefreshTokenRequired, AccessTokenRequired
from src.db.redis_db import check_jti_in_blocklist
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserInvestmentSchemaView
from src.errors import UserNotFound

# create an instance of the user service
user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:

        # get the cred details
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        # check token is valid
        if not self.token_valid(token):
            raise InvalidToken()

        # check token is not in the blocklist
        if await check_jti_in_blocklist(token_data['jti']):
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
    # verify access token is valid
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()


# created a class for raising when refresh toke is not provided
class RefreshTokenBearer(TokenBearer):
    # verify refresh token is valid
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()


# create an instance of access token bearer class
access_token_bearer = AccessTokenBearer()

# get the current user details including investment details
async def get_current_user(token_details: dict = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)) -> UserInvestmentSchemaView:
    # get the email details from token
    user_email = token_details['user']['email']

    # get the user details
    user = await user_service.get_user_by_email(user_email, session)

    if not user:
        raise UserNotFound()

    return user