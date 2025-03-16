from sqlalchemy import Column, Integer

from app.models.user_model import UserModel


class CustomerModel(UserModel):
    __tablename__ = 'customer'
    age = Column(Integer, nullable=True)
