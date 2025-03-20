import base64
from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.models.movie_images_model import MovieImagesModel
from app.models.movie_model import MovieModel
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie_images_schema import MovieImagesSchema
from app.schemas.movie_schema import MovieBaseSchema


class MovieService:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def get_all_movies(self) -> List[MovieModel]:
        return self.repository.get_all()

    def get_movie_by_id(self, movie_id: int) -> MovieModel:
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found"
            )
        return movie

    def create_movie(self, movie_data: MovieBaseSchema) -> MovieModel:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        movie_dict = movie_data.model_dump()
        movie_dict.update({
            "create_at": now,
            "update_at": now
        })
        new_movie = MovieModel(**movie_dict)
        return self.repository.create(new_movie)

    def update_movie(self, movie_id: int, movie_data: MovieBaseSchema) -> MovieModel:
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found"
            )
        update_data = movie_data.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.repository.update(movie_id, update_data)

    def delete_movie(self, movie_id: int):
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found"
            )
        self.repository.delete(movie)

    def upload_images(self, payload: MovieImagesSchema) -> MovieImagesModel:
        try:
            movie_id: int = payload.movie_id
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Movie not found")
        try:
            poster_image_data = payload.poster_image_data.split(",", 1)[1] if payload.poster_image_data.startswith(
                "data:") else payload.poster_image_data
            decoded_poster_image = base64.b64decode(poster_image_data)
            backdrop_image = payload.backdrop_image_data.split(",", 1)[1] if payload.backdrop_image_data.startswith(
                "data:") else payload.backdrop_image_data
            decoded_backdrop_image = base64.b64decode(backdrop_image)
            new_images = MovieImagesModel(movie_id=movie_id, poster_image_data=decoded_poster_image,
                                          backdrop_image_data=decoded_backdrop_image)
            return self.repository.create_movie_images(new_images)
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"An error occurred in images processing: {str(e)}")

    def get_movie_images(self, movie_id: int) -> MovieImagesModel:
        images: MovieImagesSchema = self.repository.get_movie_images(movie_id)
        if not images:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Images not found")
        return images
