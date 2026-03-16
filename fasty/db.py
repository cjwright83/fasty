import contextlib

import databases

from .config import get_settings

settings = get_settings()

if settings.db_engine in ["sqlite", "sqlite+aiosqlite"]:
    DATABASE_URL = f"{settings.db_engine}:///file.db"
else:
    DATABASE_URL = (
        f"{settings.db_engine}://"
        f"{settings.db_user}:{settings.db_password}@"
        f"{settings.db_host}/{settings.db_name}"
    )

database = databases.Database(DATABASE_URL)


@contextlib.asynccontextmanager
async def lifespan(app):
    async with database:
        await database.connect()
        yield
        await database.disconnect()
