import sqlalchemy as sa

from ..db import database

metadata = sa.MetaData()


items = sa.Table(
    "items",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(64), nullable=False),
    sa.Column("description", sa.Unicode(), nullable=False),
    sa.Column("price", sa.Numeric(), nullable=False),
    sa.Column("is_offer", sa.Boolean(), nullable=False),
)


class Item:
    @classmethod
    async def fetch_all(cls):
        return await database.fetch_all(items.select())

    @classmethod
    async def fetch_by_id(cls, id):
        return await database.fetch_one(items.select().where(items.c.id == id))

    @classmethod
    async def create(cls, **item) -> int:
        return await database.execute(items.insert().values(**item))

    @classmethod
    async def update(cls, id, **item):
        return await database.execute(
            items.update().values(**item).where(items.c.id == id)
        )

    @classmethod
    async def delete(cls, id):
        return await database.execute(items.delete().where(items.c.id == id))
