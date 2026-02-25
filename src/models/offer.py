from uuid import UUID, uuid4

from pydantic import BaseModel


class Offer(BaseModel):
    id: UUID = uuid4()
    name: str
    description: str | None = None
