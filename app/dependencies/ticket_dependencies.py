from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.service.ticket_service import TicketService


def get_ticket_repository(db: Session = Depends(get_db)):
    return TicketRepository(db)


def get_ticket_service(repository: TicketRepository = Depends(get_ticket_repository)):
    return TicketService(repository)
