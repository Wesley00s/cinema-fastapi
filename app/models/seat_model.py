from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class SeatModel(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seat_number = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    is_available = Column(Boolean, default=True)

    room = relationship("RoomModel", back_populates="seats")