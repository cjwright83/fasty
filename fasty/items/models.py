from pydantic import BaseModel, field_validator


class ItemIn(BaseModel):
    name: str
    description: str
    price: float
    is_offer: bool

    @field_validator("name", "description")
    def no_null(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("Data cannot contain null characters")
        return value


class ItemOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_offer: bool
