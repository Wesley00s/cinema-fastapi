from datetime import datetime
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    synopsis: str
    duration: int
    age_rating: str
    director: str
    release_date: str
    create_at: datetime
    update_at: datetime
