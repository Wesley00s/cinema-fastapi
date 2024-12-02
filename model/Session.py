from datetime import datetime
from pydantic import BaseModel


class Session(BaseModel):
     movie_id: int
     room_id: int
     start_time: datetime
     end_time: datetime
     price: float
     language: str
     subtitles: bool
     create_at: datetime
     update_at: datetime
