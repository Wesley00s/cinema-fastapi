from typing import List

from fastapi import HTTPException, status

from app.models.seat_model import SeatModel
from app.repositories.seat_repository import SeatRepository
from app.schemas.seat_schema import SeatBaseSchema


class SeatService:
    def __init__(self, repository: SeatRepository):
        self.repository = repository

    def get_all_seats(self) -> List[SeatModel]:
        return self.repository.get_all()

    def get_seat_by_id(self, seat_id: int) -> SeatModel:
        seat = self.repository.get_by_id(seat_id)
        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seat with id {seat_id} not found"
            )
        return seat

    def get_seats_by_room_id(self, room_id: int) -> List[SeatModel]:
        seats = self.repository.get_by_room_id(room_id)
        if not seats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with id {room_id} not found"
            )
        return seats


    def update_seat(self, seat_id: int, seat_data: SeatBaseSchema) -> SeatModel:
        seat = self.repository.get_by_id(seat_id)
        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seat with id {seat_id} not found"
            )
        update_data = seat_data.model_dump(exclude_unset=True)
        return self.repository.update(seat_id, update_data)

    def delete_seat(self, seat_id: int):
        seat = self.repository.get_by_id(seat_id)
        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seat with id {seat_id} not found"
            )
        self.repository.delete(seat)
