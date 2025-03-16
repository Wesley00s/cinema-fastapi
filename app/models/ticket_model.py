from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, UUID

from app.database.database import Base


class TicketModel(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    customer_id = Column(UUID, ForeignKey('customer.id'), nullable=False)
    seat_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
