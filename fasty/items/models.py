from pydantic import BaseModel


class ItemIn(BaseModel):
    name: str
    description: str
    price: float
    is_offer: bool


class ItemOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_offer: bool
