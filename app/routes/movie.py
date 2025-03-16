from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError

from app.dependencies.movie_dependencies import get_movie_service
from ..schemas.movie_schema import MovieBaseSchema
from ..service.movie_service import MovieService

router = APIRouter()


@router.get('/movie/all')
def get_movies(service: MovieService = Depends(get_movie_service)):
    try:
        movies = service.get_all_movies()
        return {'status': 'success', 'results': len(movies), 'movies': movies}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.post('/movie', status_code=status.HTTP_201_CREATED)
def create_movie(
        payload: MovieBaseSchema,
        service: MovieService = Depends(get_movie_service)
):
    try:
        new_movie = service.create_movie(payload)
        return {"status": "success", "movie": new_movie}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error. Check your input."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.get('/movie/{movie_id}')
def get_movie(
        movie_id: int,
        service: MovieService = Depends(get_movie_service)
):
    try:
        movie = service.get_movie_by_id(movie_id)
        return {"status": "success", "movie": movie}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.patch('/movie/{movie_id}')
def update_movie(
        movie_id: int,
        payload: MovieBaseSchema,
        service: MovieService = Depends(get_movie_service)
):
    try:
        updated_movie = service.update_movie(movie_id, payload)
        return {"status": "success", "movie": updated_movie}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error. Check your input."
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.delete('/movie/{movie_id}')
def delete_movie(
        movie_id: int,
        service: MovieService = Depends(get_movie_service)
):
    try:
        service.delete_movie(movie_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
