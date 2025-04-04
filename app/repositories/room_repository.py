from sqlalchemy.orm import Session

from app.models.room_model import RoomModel
from app.models.seat_model import SeatModel


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(RoomModel).all()

    def get_by_id(self, room_id: int):
        return self.db.query(RoomModel).get(room_id)

    def create(self, room: RoomModel):
        try:
            self.db.add(room)
            self.db.commit()
            self.db.refresh(room)
            return room
        except Exception as e:
            self.db.rollback()
            raise e

    def create_seats_for_room(self, room: RoomModel):
        try:
            for seat_number in range(1, room.capacity + 1):
                seat = SeatModel(
                    seat_number=seat_number,
                    room_id=room.id,
                    is_available=True
                )
                self.db.add(seat)
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, room_id: int, update_data: dict):
        try:
            room_query = self.db.query(RoomModel).filter(RoomModel.id == room_id)
            room = room_query.first()
            if not room:
                return None
            room_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(room)
            return room
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, room: RoomModel):
        try:
            self.db.delete(room)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
