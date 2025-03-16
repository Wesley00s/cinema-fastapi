from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.admin_repository import AdminRepository
from app.service.admin_service import AdminService


def get_admin_repository(db: Session = Depends(get_db)):
    return AdminRepository(db)


def get_admin_service(repository: AdminRepository = Depends(get_admin_repository)):
    return AdminService(repository)
