from sqlalchemy import Column, Integer, DateTime

from app.database.database import Base


class RoomModel(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
