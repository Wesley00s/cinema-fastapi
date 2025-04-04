from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.room_dependencies import get_room_repository
from app.repositories.seat_repository import SeatRepository
from app.service.seat_service import SeatService


def get_seat_repository(db: Session = Depends(get_db)):
    return SeatRepository(db)


def get_seat_service(
        repository: SeatRepository = Depends(get_seat_repository),
        room_repository: Depends = Depends(get_room_repository)
):
    return SeatService(repository, room_repository)
