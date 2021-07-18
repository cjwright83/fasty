from typing import List

from fastapi import APIRouter, HTTPException, status

from .db_models import Item
from .models import ItemIn, ItemOut

items_router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@items_router.get("/", response_model=List[ItemOut])
async def read_items():
    return await Item.fetch_all()


@items_router.get("/{id:int}/", response_model=ItemOut)
async def read_item(id: int):
    item = await Item.fetch_by_id(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@items_router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemIn):
    id = await Item.create(**item.dict())
    return {"id": id, **item.dict()}


@items_router.put("/{id:int}/", response_model=ItemOut)
async def update_item(id: int, item: ItemIn):
    await Item.update(id, **item.dict())
    return {"id": id, **item.dict()}


@items_router.delete("/{id:int}/", response_model=None)
async def delete_item(id: int):
    await Item.delete(id)
    return None
