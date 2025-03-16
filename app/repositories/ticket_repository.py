from sqlalchemy.orm import Session

from app.models.ticket_model import TicketModel


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TicketModel).all()

    def get_by_id(self, ticket_id: int):
        return self.db.query(TicketModel).get(ticket_id)

    def create(self, ticket: TicketModel):
        try:
            self.db.add(ticket)
            self.db.commit()
            self.db.refresh(ticket)
            return ticket
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, ticket_id: int, update_data: dict):
        try:
            ticket_query = self.db.query(TicketModel).filter(TicketModel.id == ticket_id)
            ticket = ticket_query.first()
            if not ticket:
                return None
            ticket_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(ticket)
            return ticket
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, ticket: TicketModel):
        try:
            self.db.delete(ticket)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
