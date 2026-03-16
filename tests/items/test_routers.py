import pytest
from faker import Faker

from fasty.items.db_models import Item

fake = Faker()


async def item(**attrs):
    await Item.create(
        name=attrs.get("name", fake.name()),
        description=attrs.get("description", fake.text()),
        price=attrs.get("price", fake.pyfloat()),
        is_offer=attrs.get("is_offer", fake.boolean()),
    )


@pytest.mark.asyncio
async def test_read_items_response_status_code_200(async_client):
    await item()
    response = await async_client.get("/items/")
    assert response.status_code == 200
