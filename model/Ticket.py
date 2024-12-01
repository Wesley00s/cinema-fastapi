from datetime import datetime


class Ticket:
    def __init__(self,
                 session_id: int,
                 user_id: int,
                 seat_number: int,
                 price: float,
                 status: str,
                 created_at: datetime,
                 updated_at: datetime):
        self.session_id = session_id
        self.user_id = user_id
        self.seat_number = seat_number
        self.price = price
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
