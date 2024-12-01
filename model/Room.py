from datetime import datetime


class Room:
    def __init__(self,
                 id: int,
                 number: int,
                 capacity: int,
                 created_at: datetime,
                 updated_at: datetime):
        self.id = id
        self.number = number
        self.capacity = capacity
        self.created_at = created_at
        self.updated_at = updated_at