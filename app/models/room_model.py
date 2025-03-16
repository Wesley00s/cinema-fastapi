from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class RoomModel(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)

    seats = relationship("SeatModel", back_populates="room", cascade="all, delete-orphan")
