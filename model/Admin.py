from model.Role import Role
from model.User import User


class Admin(User):
    role: Role = Role.ADMIN