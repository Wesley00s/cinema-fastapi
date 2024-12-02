from datetime import datetime
from pydantic import BaseModel

class Ticket(BaseModel):
     session_id: int | None = None
     customer_id: int | None = None
     seat_number: int | None = None
     price: float | None = None
     status: str | None = None
     create_at: datetime | None = None
     update_at: datetime | None = None
