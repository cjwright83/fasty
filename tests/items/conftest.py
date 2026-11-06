from collections.abc import Iterable

import pytest
from sqlmodel import Session, delete

from fasty.db import engine
from fasty.items.sql_models import Item

from .builders import build_item


@pytest.fixture
def _item_batch(request: pytest.FixtureRequest) -> Iterable[Item]:
    marker = request.node.get_closest_marker("batch_num")
    if marker is None:
        raise ValueError("batch_num marker argument missing")
    batch_num = marker.args[0]
    items = []
    with Session(engine) as session:
        while len(items) < batch_num:
            item = build_item()
            session.add(item)
            items.append(item)
        session.commit()
    yield items
    with Session(engine) as session:
        stmt = delete(Item)
        session.exec(stmt)
        session.commit()
