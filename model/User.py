class User:
    def __init__(self,
                 id: int,
                 first_name: str,
                 last_name: str,
                 address: str,
                 city: str,
                 state: str,
                 zip: str,
                 country: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country