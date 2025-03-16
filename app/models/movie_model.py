from sqlalchemy import Column, String, Integer, DateTime, Enum

from app.database.database import Base
from app.models.MovieGenre import MovieGenre


class MovieModel(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(100), nullable=False)
    genre = Column(Enum(MovieGenre), nullable=False)
    synopsis = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=False)
    age_rating = Column(Integer, nullable=False)
    director = Column(String(100), nullable=False)
    release_date = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
