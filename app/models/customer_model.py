from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.models.user_model import UserModel


class CustomerModel(UserModel):
    __tablename__ = 'customer'
    age = Column(Integer, nullable=True)

    image = relationship("CustomerImageModel", back_populates="customer", cascade="all, delete-orphan")
