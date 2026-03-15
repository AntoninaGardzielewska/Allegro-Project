from pydantic import BaseModel, AfterValidator
from typing import Annotated


def is_price(value: float) -> float:
    if value < 0:
        raise ValueError(f"{value} cannot be a negative number")
    return round(value, 2)


class Offer(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Annotated[float, AfterValidator(is_price)]
