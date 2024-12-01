from datetime import datetime


class Session:
    def __init__(self,
                 movie_id: int,
                 room_id: int,
                 start_time: datetime,
                 end_time: datetime,
                 price: float,
                 language: str,
                 subtitles: bool,
                 create_at: datetime,
                 update_at: datetime):
        self.movie_id = movie_id
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.language = language
        self.subtitles = subtitles
        self.create_at = create_at
        self.update_at = update_at
