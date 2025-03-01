import asyncio
import alembic.config
from alembic import command
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import inspect

async def migrate_to_db(script_location, alembic_ini_path="alembic.ini", connection: AsyncConnection = None, revision="head"):
    config = alembic.config.Config(alembic_ini_path)

    if connection is not None:
        config.config_ini_section = 'testdb'

        await asyncio.to_thread(command.upgrade, config, revision)
