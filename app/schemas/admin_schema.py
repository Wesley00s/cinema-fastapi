from typing import List

from pydantic import BaseModel


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
