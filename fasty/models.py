import sqlalchemy as sa

from .db import database, metadata


items = sa.Table(
    'items',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(64), nullable=False),
    sa.Column('description', sa.Unicode(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('is_offer', sa.Boolean(), nullable=False),
)


class Item:
    @classmethod
    async def fetch_all(cls):
        query = items.select()
        return await database.fetch_all(query)


    @classmethod
    async def fetch_by_id(cls, id):
        query = items.select().where(items.c.id == id)
        return await database.fetch_one(query)


    @classmethod
    async def create(cls, **item):
        query = items.insert().values(**item)
        return await database.execute(query)


    @classmethod
    async def delete(cls, id):
        query = items.delete().where(items.c.id == id)
        return await database.execute(query)
