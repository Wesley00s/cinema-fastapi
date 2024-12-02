from datetime import datetime
from pydantic import BaseModel

class Movie(BaseModel):
    title: str | None = None
    genre: str | None = None
    synopsis: str | None = None
    duration: int | None = None
    age_rating: str | None = None
    director: str | None = None
    release_date: str | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None
