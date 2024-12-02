from datetime import datetime
from pydantic import BaseModel


class Room(BaseModel):
     number: int | None = None
     capacity: int | None = None
     create_at: datetime | None = None
     update_at: datetime | None = None