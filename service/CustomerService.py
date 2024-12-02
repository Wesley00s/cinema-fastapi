from fastapi.openapi.models import Response

from model.AuthModel import AuthModel
from model.Customer import Customer
from repository.CustomerRepository import CustomerRepository
from fastapi import FastAPI, HTTPException

app = FastAPI()

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    @app.post("/customer", status_code=201)
    async def create(self, customer: Customer):
        response = self.customer_repository.save(customer)
        if response:
            return {"message": "Customer created"}
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.get("/customer/{id}")
    async def get_by_id(self, id: int):
        response = self.customer_repository.get_by_id(id)
        if response:
            return {"customer": response}
        raise HTTPException(status_code=404, detail="Customer not found")

    @app.get("/customer")
    async def get_all(self):
        response = self.customer_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=404, detail="An error occurred to fetch the data")

    @app.put("/customer/{id}")
    async def update(self, id: int, customer: Customer):
        response = self.customer_repository.update(id, customer)
        if response:
            return {"message": "Customer updated"}
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.delete("/customer/{id}")
    async def delete(self, id: int):
        response = self.customer_repository.delete(id)
        if response:
            return Response(status_code=204)
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.post("/customer/auth")
    async def auth(self, auth_model: AuthModel):
        response = self.customer_repository.authenticate(auth_model.email, auth_model.password)
        if response:
            return {"message": "Authentication successful", "customer": response}
        raise HTTPException(status_code=401, detail="Authentication failed")
