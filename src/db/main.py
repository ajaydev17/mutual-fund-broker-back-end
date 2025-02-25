from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config_obj
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# make a connection to postgres using AsyncEngine
async_engine = AsyncEngine(
    create_engine(
        url=config_obj.DATABASE_URL,
        echo=True
    )
)

# get the session object using session maker
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with session_maker() as session:
        yield session