from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from fasty.db import engine
from fasty.items.sql_models import Item

fake = Faker()


def item(**attrs):
    item = Item(
        name=attrs.get("name", fake.name()),
        description=attrs.get("description", fake.text()),
        price=attrs.get("price", fake.pyfloat()),
        is_offer=attrs.get("is_offer", fake.boolean()),
    )
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item


def test_read_items_response_status_code_200(client: TestClient):
    item()
    response = client.get("/items/")
    assert response.status_code == 200
