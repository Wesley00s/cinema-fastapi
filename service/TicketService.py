from datetime import datetime

from fastapi import FastAPI, HTTPException

from model.Ticket import Ticket
from repository.CustomerRepository import CustomerRepository
from repository.SessionRepository import SessionRepository
from repository.TicketRepository import TicketRepository

app = FastAPI()

class TicketService:
    def __init__(self,
                 ticket_repository: TicketRepository,
                 session_repository: SessionRepository,
                 customer_repository: CustomerRepository
                 ):
        self.ticket_repository = ticket_repository
        self.session_repository = session_repository
        self.customer_repository = customer_repository

    @app.post("/ticket")
    async def create(self, ticket: Ticket):
        existing_session = self.session_repository.get_by_id(ticket.session_id)
        existing_customer = self.customer_repository.get_by_id(ticket.customer_id)

        if existing_session is None:
            raise HTTPException(status_code=404, detail=f"Session with id {ticket.session_id} not found")
        if existing_customer is None:
            raise HTTPException(status_code=404, detail=f"Customer with id {ticket.customer_id} not found")

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticket.create_at = now
        ticket.update_at = now

        response = self.ticket_repository.save(ticket)
        if response:
            return {"message": "Ticket created successfully"}
        raise HTTPException(status_code=500, detail="Ticket could not be created")

    @app.get("/ticket")
    async def get_all(self):
        response = self.ticket_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=500, detail="All tickets could not be found")

    @app.get("/ticket/{id}")
    async def get_by_id(self, id: int):
        response = self.ticket_repository.get_by_id(id)
        if response:
            return response
        raise HTTPException(status_code=500, detail="Ticket could not be found")

    @app.put("/ticket/{id}")
    async def update(self, id: int, ticket: Ticket):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticket.update_at = now
        response = self.ticket_repository.update(id, ticket)
        if response:
            return {"message": "Ticket updated successfully"}
        raise HTTPException(status_code=500, detail="Ticket could not be updated")

    @app.delete("/ticket/{id}")
    async def delete(self, id: int):
        response = self.ticket_repository.delete(id)
        if response:
            return {"message": "Ticket deleted successfully"}
        raise HTTPException(status_code=500, detail="Ticket could not be deleted")