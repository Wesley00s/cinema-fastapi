import base64
from datetime import timedelta
from typing import List
from uuid import UUID

import bcrypt
from fastapi import HTTPException, status

from app.core.db_config import settings
from app.core.security import create_access_token
from app.models.admin_image_model import AdminImageModel
from app.models.admin_model import AdminModel
from app.models.auth_model import AuthModel
from app.repositories.admin_repository import AdminRepository
from app.schemas.admin_image_schema import AdminImageSchema
from app.schemas.admin_schema import AdminBaseSchema
from app.schemas.reset_password_schema import ResetPasswordSchema


class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_all_admins(self) -> List[AdminModel]:
        return self.repository.get_all()

    def get_admin_by_id(self, admin_id: UUID) -> AdminModel:
        admin = self.repository.get_by_id(admin_id)
        if not admin:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin

    def get_admin_by_email(self, email: str) -> AdminModel:
        admin = self.repository.get_by_email(email)
        if not admin:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin

    def create_admin(self, payload: AdminBaseSchema):
        hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_data = payload.model_dump(exclude={"password"})
        admin_data.update({"password": hashed_password})

        try:
            new_admin = AdminModel(**admin_data)
            created_admin = self.repository.create(new_admin)
            access_token = self._generate_access_token(created_admin)
            return {"admin": created_admin, "access_token": access_token}
        except ValueError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

    def update_admin(self, admin_id: UUID, payload: AdminBaseSchema) -> AdminModel:
        update_data = payload.model_dump(exclude_unset=True)
        return self.repository.update(admin_id, update_data)

    def delete_admin(self, admin_id: UUID):
        admin = self.repository.get_by_id(admin_id)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Admin with id {admin_id} not found"
            )
        self.repository.delete(admin)

    def reset_password(self, payload: ResetPasswordSchema):
        admin = self.repository.get_by_email(payload.email)
        if not admin:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Admin not found")

        hashed_password = bcrypt.hashpw(payload.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.repository.update(admin.id, {"password": hashed_password})
        return {"message": "Password has been reset successfully"}

    def authenticate_admin(self, payload: AuthModel):
        admin = self.repository.get_by_email(payload.email)
        if not admin or not bcrypt.checkpw(payload.password.encode('utf-8'), admin.password.encode('utf-8')):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return self._generate_access_token(admin)

    def upload_image(self, payload: AdminImageSchema):
        try:
            admin_id = UUID(payload.admin_id)
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

        admin = self.repository.get_by_id(admin_id)
        if not admin:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Admin not found")

        try:
            image_data = payload.image_data.split(",", 1)[1] if payload.image_data.startswith(
                "data:") else payload.image_data
            decoded_image = base64.b64decode(image_data)
            new_image = AdminImageModel(admin_id=admin_id, image_data=decoded_image)
            return self.repository.create_admin_image(new_image)
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"An error occurred in image processing: {str(e)}")

    def get_admin_image(self, admin_id: UUID):
        image = self.repository.get_admin_image(admin_id)
        if not image:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
        return image.image_data

    def _generate_access_token(self, admin: AdminModel):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": admin.email, "id": str(admin.id)},
            expires_delta=access_token_expires
        )
