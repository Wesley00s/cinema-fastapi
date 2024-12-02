from datetime import datetime

from fastapi import FastAPI, HTTPException

from model.Room import Room
from repository.RoomRepository import RoomRepository

app = FastAPI()

class RoomService:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    @app.post("/room", status_code=201)
    async def create(self, room: Room):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        room.create_at = now
        room.update_at = now

        response = self.room_repository.save(room)
        if response:
            return {"message": "Room created successfully"}
        raise HTTPException(status_code=404, detail="Cannot create room.")

    @app.get("/room/{id}")
    async def get_by_id(self, id: int):
        response = self.room_repository.get_by_id(id)
        if response:
            return response
        raise HTTPException(status_code=404, detail=f"Cannot find room with given id {id}.")

    @app.get("/room")
    async def get_all(self):
        response = self.room_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=404, detail=f"Cannot find all rooms.")

    @app.put("/room/{id}")
    async def update(self, id: int,  room: Room):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        room.update_at = now

        response = self.room_repository.update(id, room)
        if response:
            return {"message": "Room updated successfully"}
        raise HTTPException(status_code=404, detail=f"Cannot update room with given id {id}.")

    @app.delete("/room/{id}")
    async def delete(self, id: int):
        response = self.room_repository.delete(id)
        if response:
            return {"message": "Room deleted successfully"}
        raise HTTPException(status_code=404, detail=f"Cannot find room with given id {id}.")