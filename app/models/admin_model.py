from app.models.user_model import UserModel


class AdminModel(UserModel):
    __tablename__ = 'admin'
    pass
