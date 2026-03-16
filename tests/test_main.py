import pytest


@pytest.mark.asyncio
async def test_read_main_response_status_code_200(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_main_response_json(async_client):
    response = await async_client.get("/")
    assert response.json() == {"Hello": "World"}
