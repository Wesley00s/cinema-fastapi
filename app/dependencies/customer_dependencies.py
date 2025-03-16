from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.service.customer_service import CustomerService


def get_customer_repository(db: Session = Depends(get_db)):
    return CustomerRepository(db)


def get_customer_service(repository: CustomerRepository = Depends(get_customer_repository)):
    return CustomerService(repository)
