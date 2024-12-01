from model.User import User


class Admin(User):
    def __init__(self,
                 email: str,
                 password: str,
                 id: int,
                 first_name: str,
                 last_name: str,
                 address: str,
                 city: str,
                 state: str,
                 zip: str,
                 country: str):
        super().__init__(id, first_name, last_name, address, city, state, zip, country)
        self.email = email
        self.password = password