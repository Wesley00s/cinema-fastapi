from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.customer_image_model import CustomerImageModel
from app.models.customer_model import CustomerModel


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(CustomerModel).all()

    def get_by_id(self, customer_id: UUID):
        return self.db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()

    def get_by_email(self, email: str):
        return self.db.query(CustomerModel).filter(CustomerModel.email == email).first()

    def create(self, customer: CustomerModel):
        try:
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            return customer
        except IntegrityError as e:
            self.db.rollback()
            raise e

    def update(self, customer_id: UUID, update_data: dict):
        try:
            customer_query = self.db.query(CustomerModel).filter(CustomerModel.id == customer_id)
            customer = customer_query.first()
            if not customer:
                return None
            customer_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(customer)
            return customer
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, customer: CustomerModel):
        try:
            self.db.delete(customer)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def create_customer_image(self, image: CustomerImageModel):
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_customer_image(self, customer_id: UUID):
        return self.db.query(CustomerImageModel).filter(CustomerImageModel.customer_id == customer_id).first()
