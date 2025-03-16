from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.session_repository import SessionRepository
from app.service.session_service import SessionService


def get_session_repository(db: Session = Depends(get_db)):
    return SessionRepository(db)


def get_session_service(repository: SessionRepository = Depends(get_session_repository)):
    return SessionService(repository)
