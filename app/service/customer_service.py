import base64
from datetime import timedelta
from typing import List
from uuid import UUID

import bcrypt
from fastapi import HTTPException, status

from app.core.db_config import settings
from app.core.security import create_access_token
from app.models.auth_model import AuthModel
from app.models.customer_image_model import CustomerImageModel
from app.models.customer_model import CustomerModel
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer_image_schema import CustomerImageSchema
from app.schemas.customer_schema import CustomerBaseSchema
from app.schemas.reset_password_schema import ResetPasswordSchema


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all_customers(self) -> List[CustomerModel]:
        return self.repository.get_all()

    def get_customer_by_id(self, customer_id: UUID) -> CustomerModel:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    def get_customer_by_email(self, email: str) -> CustomerModel:
        customer = self.repository.get_by_email(email)
        if not customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    def create_customer(self, payload: CustomerBaseSchema):
        hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        customer_data = payload.model_dump(exclude={"password"})
        customer_data.update({"password": hashed_password})

        try:
            new_customer = CustomerModel(**customer_data)
            created_customer = self.repository.create(new_customer)
            access_token = self._generate_access_token(created_customer)
            return {"customer": created_customer, "access_token": access_token}
        except ValueError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

    def update_customer(self, customer_id: UUID, payload: CustomerBaseSchema) -> CustomerModel:
        update_data = payload.model_dump(exclude_unset=True)
        return self.repository.update(customer_id, update_data)

    def delete_customer(self, customer_id: UUID):
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found"
            )
        self.repository.delete(customer)

    def reset_password(self, payload: ResetPasswordSchema):
        customer = self.repository.get_by_email(payload.email)
        if not customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Customer not found")

        hashed_password = bcrypt.hashpw(payload.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.repository.update(customer.id, {"password": hashed_password})
        return {"message": "Password has been reset successfully"}

    def authenticate_customer(self, payload: AuthModel):
        customer = self.repository.get_by_email(payload.email)
        if not customer or not bcrypt.checkpw(payload.password.encode('utf-8'), customer.password.encode('utf-8')):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return self._generate_access_token(customer)

    def upload_image(self, payload: CustomerImageSchema):
        try:
            customer_id = UUID(payload.customer_id)
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Customer not found")

        try:
            image_data = payload.image_data.split(",", 1)[1] if payload.image_data.startswith(
                "data:") else payload.image_data
            decoded_image = base64.b64decode(image_data)
            new_image = CustomerImageModel(customer_id=customer_id, image_data=decoded_image)
            return self.repository.create_customer_image(new_image)
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"An error occurred in image processing: {str(e)}")

    def get_customer_image(self, customer_id: UUID):
        image = self.repository.get_customer_image(customer_id)
        if not image:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Image not found")
        return image.image_data

    def _generate_access_token(self, customer: CustomerModel):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": customer.email, "id": str(customer.id)},
            expires_delta=access_token_expires
        )
