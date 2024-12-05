from datetime import datetime

from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/movie')
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return {'status': 'success', 'results': len(movies), 'movies': movies}


@router.post('/movie', status_code=status.HTTP_201_CREATED)
def create_movie(payload: schemas.MovieBaseSchema, db: Session = Depends(get_db)):
    new_movie = models.Movie(**payload.model_dump())
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_movie.create_at = now
    new_movie.update_at = now
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return {"status": "success", "movie": new_movie}


@router.get('/movie/{id}')
def get_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No movie with this id: {id} found")
    return {"status": "success", "movie": movie}


@router.patch('/movie/{id}')
def update_movie(id: int, payload: schemas.MovieBaseSchema, db: Session = Depends(get_db)):
    movie_query = db.query(models.Movie).filter(models.Movie.id == id)
    db_movie = movie_query.first()

    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No movie with this id: {id} found')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_movie.update_at = now
    update_data = payload.model_dump(exclude_unset=True)
    movie_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_movie)
    return {"status": "success", "movie": db_movie}


@router.delete('/movie/{id}')
def delete_movie(id: int, db: Session = Depends(get_db)):
    movie_query = db.query(models.Movie).filter(models.Movie.id == id)
    movie = movie_query.first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No movie with this id: {id} found')
    movie_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
