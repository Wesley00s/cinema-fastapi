from sqlalchemy import Column, Integer, ForeignKey, UUID, LargeBinary
from sqlalchemy.orm import relationship

from app.database.database import Base


class CustomerImageModel(Base):
    __tablename__ = 'customer_image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customer.id'), nullable=False)
    image_data = Column(LargeBinary, nullable=False)

    customer = relationship("CustomerModel", back_populates="image")