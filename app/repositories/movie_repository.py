from sqlalchemy.orm import Session

from app.models.movie_model import MovieModel


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(MovieModel).all()

    def get_by_id(self, movie_id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    def create(self, movie: MovieModel):
        try:
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, movie_id: int, update_data: dict):
        try:
            movie_query = self.db.query(MovieModel).filter(MovieModel.id == movie_id)
            movie = movie_query.first()
            if not movie:
                return None
            movie_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, movie: MovieModel):
        try:
            self.db.delete(movie)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
