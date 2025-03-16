from datetime import datetime
from typing import List

from pydantic import BaseModel


class SeatBaseSchema(BaseModel):
    id: int | None = None
    room_id: int | None = None
    is_available: bool = True

    class Config:
        from_attributes = True
        populate_by_name = True