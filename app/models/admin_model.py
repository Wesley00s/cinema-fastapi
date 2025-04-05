from sqlalchemy.orm import relationship

from app.models.user_model import UserModel


class AdminModel(UserModel):
    __tablename__ = 'admin'
    pass

    image = relationship("AdminImageModel", back_populates="admin", cascade="all, delete-orphan")
