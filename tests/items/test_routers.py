from collections.abc import Iterable

import pytest
from fastapi.testclient import TestClient

from fasty.items.sql_models import Item


def test_read_items_response_status_code_200(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200


@pytest.mark.batch_num(5)
def test_read_items_returns_the_list_of_total_items(
    client: TestClient, _item_batch: Iterable[Item]
):
    response = client.get("/items/")
    assert len(response.json()) == 5
