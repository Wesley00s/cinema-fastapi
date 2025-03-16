from datetime import datetime
from typing import List

from pydantic import BaseModel


class RoomBaseSchema(BaseModel):
    number: int | None = None
    capacity: int | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class RoomSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[RoomBaseSchema]
