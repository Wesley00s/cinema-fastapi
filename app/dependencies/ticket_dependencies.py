from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.customer_dependencies import get_customer_repository
from app.dependencies.movie_dependencies import get_movie_repository
from app.dependencies.session_dependencies import get_session_repository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.movie_repository import MovieRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.ticket_repository import TicketRepository
from app.service.ticket_service import TicketService


def get_ticket_repository(db: Session = Depends(get_db)):
    return TicketRepository(db)


def get_ticket_service(
        repository: TicketRepository = Depends(get_ticket_repository),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        movie_repository: MovieRepository = Depends(get_movie_repository),
        session_repository: SessionRepository = Depends(get_session_repository)
):
    return TicketService(repository, customer_repository, movie_repository, session_repository)
