from datetime import datetime


class Movie:
    def __init__(self,
                 id: int,
                 title: str,
                 genre: str,
                 synopsis: str,
                 duration: int,
                 age_rating: str,
                 director: str,
                 cast: list,
                 release_date: str,
                 create_at: datetime,
                 update_at: datetime):
        self.id = id
        self.title = title
        self.genre = genre
        self.synopsis = synopsis
        self.duration = duration
        self.age_rating = age_rating
        self.director = director
        self.cast = cast
        self.release_date = release_date
        self.create_at = create_at
        self.update_at = update_at
