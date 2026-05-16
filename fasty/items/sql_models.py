from collections.abc import Callable
from typing import Any, ClassVar

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    __tablename__: ClassVar[str | Callable[..., str]] = "items"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: int
    is_offer: bool

    def update(self, item_attrs: dict[str, Any]) -> None:
        pass
