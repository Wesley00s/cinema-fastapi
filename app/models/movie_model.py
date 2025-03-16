from sqlalchemy import Column, String, Integer, DateTime

from app.database.database import Base


class MovieModel(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    synopsis = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    age_rating = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
