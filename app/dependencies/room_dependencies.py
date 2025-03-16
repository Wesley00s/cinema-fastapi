from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.room_repository import RoomRepository
from app.service.room_service import RoomService


def get_room_repository(db: Session = Depends(get_db)):
    return RoomRepository(db)


def get_room_service(repository: RoomRepository = Depends(get_room_repository)):
    return RoomService(repository)
