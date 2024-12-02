from datetime import datetime
from pydantic import BaseModel

class Ticket(BaseModel):
     session_id: int
     user_id: int
     seat_number: int
     price: float
     status: str
     created_at: datetime
     updated_at: datetime
