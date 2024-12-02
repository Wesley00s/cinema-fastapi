from fastapi import HTTPException, FastAPI
from fastapi.openapi.models import Response

from model.Admin import Admin
from model.AuthModel import AuthModel
from repository.AdminRepository import AdminRepository

app = FastAPI()

class AdminService:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    @app.post("/admin", status_code=201)
    async def create(self, admin: Admin):
        response = self.admin_repository.save(admin)
        if response:
            return {"message": "Admin created"}
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.get("/admin/{id}")
    async def get_by_id(self, id: int):
        response = self.admin_repository.get_by_id(id)
        if response:
            return {"admin": response}
        raise HTTPException(status_code=404, detail="Admin not found")

    @app.get("/admin")
    async def get_all(self):
        response = self.admin_repository.get_all()
        if response:
            return response
        raise HTTPException(status_code=404, detail="An error occurred to fetch the data")

    @app.put("/admin/{id}")
    async def update(self, id: int, admin: Admin):
        response = self.admin_repository.update(id, admin)
        if response:
            return {"message": "Admin updated"}
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.delete("/admin/{id}")
    async def delete(self, id: int):
        response = self.admin_repository.delete(id)
        if response:
            return Response(status_code=204)
        raise HTTPException(status_code=500, detail="Something went wrong")

    @app.post("/admin/auth")
    async def auth(self, auth_model: AuthModel):
        response = self.admin_repository.authenticate(auth_model.email, auth_model.password)
        if response:
            return {"message": "Authentication successful", "admin": response}
        raise HTTPException(status_code=401, detail="Authentication failed")
