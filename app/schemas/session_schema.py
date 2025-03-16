from datetime import datetime
from typing import List

from pydantic import BaseModel


class SessionBaseSchema(BaseModel):
    movie_id: int | None = None
    room_number: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    price: float | None = None
    language: str | None = None
    subtitles: bool | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class SessionSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[SessionBaseSchema]
