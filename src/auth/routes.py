from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserViewSchema, UserCreateSchema, UserLoginSchema
from src.auth.services import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.errors import UserAlreadyExists
from src.auth.utils import create_access_token, verify_password_hash


# define the router
auth_router = APIRouter()

# create a user service instance
user_service = UserService()

# create the routes below
@auth_router.post('/signup', response_model=UserViewSchema, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateSchema,
                              session: AsyncSession = Depends(get_session)) -> UserViewSchema:
    # get the email address
    email = user_data.email

    # check user already exists
    is_user_exists = await user_service.get_user_by_email(email, session)

    if is_user_exists:
        raise UserAlreadyExists()

    user = await user_service.create_user(user_data, session)
    return user

@auth_router.post('/login')
async def login(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)) -> dict:
    # get the email and password
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        is_password_valid = verify_password_hash(password, user.password_hash)

        if is_password_valid:
            access_token =


