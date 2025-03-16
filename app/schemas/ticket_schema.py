from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class TicketBaseSchema(BaseModel):
    session_id: int | None = None
    customer_id: UUID | None = None
    seat_number: int | None = None
    price: float | None = None
    status: str | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class TicketSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[TicketBaseSchema]
