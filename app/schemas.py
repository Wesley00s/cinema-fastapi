from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CustomerBaseSchema(BaseModel):
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
    age: int | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class CustomerSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[CustomerBaseSchema]

class AdminBaseSchema(BaseModel):
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class AdminSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[AdminBaseSchema]


class CustomerImageSchema(BaseModel):
    customer_id: str
    image_data: str

    class Config:
        orm_mode = True


class AdminImageSchema(BaseModel):
    admin_id: str
    image_data: str

    class Config:
        orm_mode = True


class MovieBaseSchema(BaseModel):
    title: str | None = None
    genre: str | None = None
    synopsis: str | None = None
    duration: int | None = None
    age_rating: int | None = None
    director: str | None = None
    release_date: datetime | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class MovieSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[MovieBaseSchema]

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

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class ResetPasswordSchema(BaseModel):
    email: str
    new_password: str