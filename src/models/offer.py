from pydantic import BaseModel


class Offer(BaseModel):
    id: int
    name: str
    description: str | None = None
