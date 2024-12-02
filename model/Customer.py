from model.Role import Role
from model.User import User


class Customer(User):
    age: int | None = None
    role: Role = Role.CUSTOMER
