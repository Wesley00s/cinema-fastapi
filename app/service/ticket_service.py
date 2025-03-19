from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.models.customer_model import CustomerModel
from app.models.movie_model import MovieModel
from app.models.session_model import SessionModel
from app.models.ticket_model import TicketModel
from app.repositories.customer_repository import CustomerRepository
from app.repositories.movie_repository import MovieRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketBaseSchema


class TicketService:
    def __init__(
            self,
            repository: TicketRepository,
            customer_repository: CustomerRepository,
            movie_repository: MovieRepository,
            session_repository: SessionRepository
    ):
        self.repository = repository
        self.customer_repository = customer_repository
        self.movie_repository = movie_repository
        self.session_repository = session_repository

    def get_all_tickets(self) -> List[TicketModel]:
        return self.repository.get_all()

    def get_ticket_by_id(self, ticket_id: int) -> TicketModel:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found"
            )
        return ticket

    def create_ticket(self, ticket_data: TicketBaseSchema) -> TicketModel:
        customer: CustomerModel = self.customer_repository.get_by_id(ticket_data.customer_id)
        session: SessionModel = self.session_repository.get_by_id(ticket_data.session_id)
        movie: MovieModel = self.movie_repository.get_by_id(session.movie_id)

        if customer.age < movie.age_rating:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Customer age is less than movie age rating."
            )

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticket_dict = ticket_data.model_dump()
        ticket_dict.update({
            "create_at": now,
            "update_at": now
        })
        new_ticket = TicketModel(**ticket_dict)
        return self.repository.create(new_ticket)

    def update_ticket(self, ticket_id: int, ticket_data: TicketBaseSchema) -> TicketModel:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found"
            )
        update_data = ticket_data.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.repository.update(ticket_id, update_data)

    def delete_ticket(self, ticket_id: int):
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found"
            )
        self.repository.delete(ticket)
