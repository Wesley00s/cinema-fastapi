from sqlalchemy.orm import Session

from app.models.room_model import RoomModel
from app.models.seat_model import SeatModel


class SeatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(SeatModel).all()

    def get_by_number(self, seat_number: int):
        return self.db.query(SeatModel).filter(SeatModel.seat_number == seat_number).first()

    def get_by_room_id(self, room_id: int):
        return self.db.query(SeatModel).filter(SeatModel.room_id == room_id).all()

    def get_by_room_number(self, room_number: int):
        try:
            room_query = self.db.query(RoomModel).filter(RoomModel.number == room_number)
            room = room_query.first()
            if not room:
                return None
            seat_query = self.db.query(SeatModel).filter(SeatModel.room_id == room.id)
            return seat_query.all()
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, seat_number: int, update_data: dict):
        try:
            seat_query = self.db.query(SeatModel).filter(SeatModel.seat_number == seat_number)
            seat = seat_query.first()
            if not seat:
                return None
            seat_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(seat)
            return seat
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, seat: SeatModel):
        try:
            self.db.delete(seat)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
