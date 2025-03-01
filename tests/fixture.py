import pytest
from tests.utils import docker_utils
from tests.utils import database_utils

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from httpx import AsyncClient, ASGITransport
from src import app
from src.db.main import get_session
import asyncio
from unittest.mock import AsyncMock


from src.config import config_obj

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def db_session():
    # Start the database container
    container = docker_utils.start_database_container()

    # Create an async engine
    async_engine = create_async_engine(
        config_obj.TEST_DATABASE_URL,
        echo=True
    )

    async with async_engine.connect() as connection:
        await database_utils.migrate_to_db("migrations", "alembic.ini", connection)

    session_maker = sessionmaker(autocommit=False, autoflush=True, bind=async_engine, class_=AsyncSession)

    async with session_maker() as session:
        yield session

    # stopping the container once test is done
    # container.stop()
    # container.remove()

    await async_engine.dispose()



@pytest.fixture(scope='function')
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://localhost') as client:
        yield client

@pytest.fixture(scope="function")
async def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    app.dependency_overrides[get_session] = lambda: mock_session
    yield mock_session
    app.dependency_overrides.clear()