import pytest
from httpx import AsyncClient, ASGITransport

from ..main import app


def assert_equal(expected, actual) -> None:
    assert expected == actual


@pytest.mark.asyncio
async def test_read_main_response_status_code_200():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert_equal(200, response.status_code)


@pytest.mark.asyncio
async def test_read_main_response_json():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert_equal({"Hello": "World"}, response.json())
