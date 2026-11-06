from collections.abc import Sequence
from typing import Any

from sqlmodel import Session, select

from ..db import engine
from .sql_models import Item


def fetch_all_items() -> Sequence[Item]:
    with Session(engine) as session:
        return session.exec(select(Item)).all()


def fetch_one_item_by_id(id: int) -> Item | None:
    with Session(engine) as session:
        return session.get(Item, id)


def create_new_item(item_attrs: dict[str, Any]) -> Item:
    item = Item(**item_attrs)
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item


def update_existing_item(id: int, item_attrs: dict[str, Any]) -> Item | None:
    with Session(engine) as session:
        item = session.get(Item, id)
        if not item:
            return None
        item.update(item_attrs)
        session.add(item)
        session.commit()
        session.refresh(item)
    return item


def destroy_item(id: int) -> Item | None:
    with Session(engine) as session:
        item = session.get(Item, id)
        if not item:
            return None
        session.delete(item)
        session.commit()
    return item
