import databases
from sqlalchemy import MetaData

from .config import get_settings

settings = get_settings()

DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}'

database = databases.Database(DATABASE_URL)

metadata = MetaData()


async def database_connect() -> None:
    await database.connect()


async def database_disconnect() -> None:
    await database.disconnect()
