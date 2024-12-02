from datetime import datetime

from fastapi import FastAPI, HTTPException

from model.Session import Session
from repository.MovieRepository import MovieRepository
from repository.RoomRepository import RoomRepository
from repository.SessionRepository import SessionRepository

app = FastAPI()

class SessionService:
    def __init__(self,
                 session_repository: SessionRepository,
                 room_repository: RoomRepository,
                 movie_repository: MovieRepository,
                 ):
        self.session_repository = session_repository
        self.room_repository = room_repository
        self.movie_repository = movie_repository

    @app.post("/session")
    async def create(self, session: Session):
        existing_room = self.room_repository.get_by_id(session.room_id)
        existing_movie = self.movie_repository.get_by_id(session.movie_id)

        if existing_room is None:
            raise HTTPException(status_code=404, detail=f"Room with id {session.room_id} not found")
        if existing_movie is None:
            raise HTTPException(status_code=404, detail=f"Movie with id {session.movie_id} not found")

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session.create_at = now
        session.update_at = now

        response = self.session_repository.save(session)
        if response:
            return {"message": "Session created successfully."}
        raise HTTPException(status_code=500, detail="An error occurred to create session.")

    @app.get("/session")
    async def get_all(self):
        response = self.session_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=500, detail="An error occurred to get all session.")

    @app.get("/session/{id}")
    async def get_by_id(self, id: int):
        response = self.session_repository.get_by_id(id)
        if response:
            return response
        raise HTTPException(status_code=500, detail="An error occurred to get a session by id.")

    @app.put("/session/{id}")
    async def update(self, id: int, session: Session):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session.update_at = now

        response = self.session_repository.update(id, session)
        if response:
            return {"message": "Session updated successfully."}
        raise HTTPException(status_code=500, detail="An error occurred to update session.")

    @app.delete("/session/{id}")
    async def delete(self, id: int):
        response = self.session_repository.delete(id)
        if response:
            return {"message": "Session deleted successfully."}
        raise HTTPException(status_code=500, detail="An error occurred to delete a session.")