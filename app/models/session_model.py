from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Boolean

from app.database.database import Base


class SessionModel(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    room_number = Column(Integer, ForeignKey('room.number'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    language = Column(String, nullable=False)
    subtitles = Column(Boolean, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
