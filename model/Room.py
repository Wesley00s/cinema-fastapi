from datetime import datetime
from pydantic import BaseModel


class Room(BaseModel):
     id: int
     number: int
     capacity: int
     created_at: datetime
     updated_at: datetime