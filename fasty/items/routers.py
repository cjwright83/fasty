from fastapi import APIRouter, HTTPException, Path, status

from .models import ItemIn, ItemOut
from .service import (
    create_new_item,
    destroy_item,
    fetch_all_items,
    fetch_one_item_by_id,
    update_existing_item,
)

items_router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@items_router.get("/", response_model=list[ItemOut])
def read_items():
    return fetch_all_items()


@items_router.get("/{id:int}/", response_model=ItemOut)
def read_item(
    id: int = Path(..., title="The ID of the item to get.", ge=1, le=2**31),
):
    item = fetch_one_item_by_id(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@items_router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemIn):
    item = create_new_item(item_in.model_dump())
    return item


@items_router.put("/{id:int}/", response_model=ItemOut)
def update_item(
    item_in: ItemIn,
    id: int = Path(..., title="The ID of the item to update.", ge=1, le=2**31),
):
    update_existing_item(id, **item_in.model_dump())
    return {"id": id, **item_in.model_dump()}


@items_router.delete("/{id:int}/", response_model=None)
def delete_item(
    id: int = Path(..., title="The ID of the item to delete.", ge=1, le=2**31),
):
    item = destroy_item(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
