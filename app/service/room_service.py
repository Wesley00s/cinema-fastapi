from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.models.room_model import RoomModel
from app.repositories.room_repository import RoomRepository
from app.schemas.room_schema import RoomBaseSchema


class RoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def get_all_rooms(self) -> List[RoomModel]:
        return self.repository.get_all()

    def get_room_by_id(self, room_id: int) -> RoomModel:
        room = self.repository.get_by_id(room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with id {room_id} not found"
            )
        return room

    def create_room(self, room_data: RoomBaseSchema) -> RoomModel:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        room_dict = room_data.model_dump()
        room_dict.update({
            "create_at": now,
            "update_at": now,
        })
        new_room = RoomModel(**room_dict)
        return self.repository.create(new_room)

    def update_room(self, room_id: int, room_data: RoomBaseSchema) -> RoomModel:
        room = self.repository.get_by_id(room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with id {room_id} not found"
            )
        update_data = room_data.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.repository.update(room_id, update_data)

    def delete_room(self, room_id: int):
        room = self.repository.get_by_id(room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with id {room_id} not found"
            )
        self.repository.delete(room)
