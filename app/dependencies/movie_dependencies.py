from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.service.movie_service import MovieService


def get_movie_repository(db: Session = Depends(get_db)):
    return MovieRepository(db)


def get_movie_service(repository: MovieRepository = Depends(get_movie_repository)):
    return MovieService(repository)
