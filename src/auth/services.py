from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.auth.schemas import UserViewSchema, UserCreateSchema, UserLoginSchema
from src.auth.utils import generate_password_hash


# all the user related services
class UserService:

    # get user by email
    async def get_user_by_email(self, email: str, session: AsyncSession) -> UserViewSchema:
        statement = select(User).where(User.email==email)
        result = await session.exec(statement)
        user = result.first()
        return user

    # create user using email and password
    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> UserViewSchema:
        # create a dictionary of user info
        user_data_dict = user_data.model_dump()
        user = User(**user_data_dict)

        # generate password hash
        password = generate_password_hash(user_data_dict['password'])
        user.password_hash = password

        # add user to db
        session.add(user)
        await session.commit()
        return user

    # update user details
    async def update_user(self, user: UserViewSchema, user_data: dict, session: AsyncSession) -> UserViewSchema:
        # update the values in the user_data to user
        for key, value in user_data.items():
            setattr(user, key, value)

        # commit to the db
        await session.commit()
        return user