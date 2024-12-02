from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.openapi.models import Response

from model.Movie import Movie
from repository.MovieRepository import MovieRepository

app = FastAPI()

class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @app.post("/movie", status_code=201)
    async def create(self, movie: Movie):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        movie.create_at = now
        movie.update_at = now

        response = self.movie_repository.save(movie)
        if response:
            return {"message": "Movie created successfully"}
        raise HTTPException(status_code=404, detail="An error occurred to create the movie")

    @app.get("/movie")
    async def get_all(self):
        response = self.movie_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=404, detail="An error occurred to get response")

    @app.get("/movie/{id}")
    async def get_by_id(self, id):
        response = self.movie_repository.get_by_id(id)
        if response:
            return response
        raise HTTPException(status_code=404, detail="An error occurred to get response")

    @app.put("/movie/{id}")
    async def update(self, id: int, movie: Movie):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        movie.update_at = now
        response = self.movie_repository.update(id, movie)
        if response:
            return {'message': 'Movie updated successfully'}
        raise HTTPException(status_code=404, detail="An error occurred to update the movie")

    @app.delete("/movie/{id}")
    async def delete(self, id):
        response = self.movie_repository.delete(id)
        if response:
            return {"message": "Movie deleted successfully"}
        raise HTTPException(status_code=404, detail="An error occurred to delete movie")
