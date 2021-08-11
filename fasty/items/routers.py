from typing import List

from fastapi import APIRouter, HTTPException, Path, status

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
async def read_item(
    id: int = Path(..., title="The ID of the item to get.", ge=1, le=2 ** 31),
):
    item = await Item.fetch_by_id(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@items_router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemIn):
    id = await Item.create(**item.dict())
    return {"id": id, **item.dict()}


@items_router.put("/{id:int}/", response_model=ItemOut)
async def update_item(
    item: ItemIn,
    id: int = Path(..., title="The ID of the item to update.", ge=1, le=2 ** 31),
):
    await Item.update(id, **item.dict())
    return {"id": id, **item.dict()}


@items_router.delete("/{id:int}/", response_model=None)
async def delete_item(
    id: int = Path(..., title="The ID of the item to delete.", ge=1, le=2 ** 31),
):
    await Item.delete(id)
    return None
