from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)

from fasty import db_models
from fasty.db import DATABASE_URL
from fasty.main import app

# Need to add interface for adding records.

async_engine = create_async_engine(
    DATABASE_URL, pool_size=10, echo=True, max_overflow=10
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    metadata = db_models.metadata
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        yield


@pytest_asyncio.fixture(scope="module")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
