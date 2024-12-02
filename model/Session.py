from datetime import datetime
from pydantic import BaseModel


class Session(BaseModel):
     movie_id: int | None = None
     room_id: int | None = None
     start_time: datetime | None = None
     end_time: datetime | None = None
     price: float | None = None
     language: str | None = None
     subtitles: bool | None = None
     create_at: datetime | None = None
     update_at: datetime | None = None
