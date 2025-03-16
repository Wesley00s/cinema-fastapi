from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.models.ticket_model import TicketModel
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketBaseSchema


class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

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
