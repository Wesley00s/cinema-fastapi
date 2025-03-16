from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.MovieGenre import MovieGenre


class MovieBaseSchema(BaseModel):
    title: str | None = None
    genre: MovieGenre | None = None
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
        use_enum_values = True
        arbitrary_types_allowed = True


class MovieSchemeResponse(BaseModel):
    status: str
    result: int
    notes: List[MovieBaseSchema]
