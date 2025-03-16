from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.models.session_model import SessionModel
from app.repositories.session_repository import SessionRepository
from app.schemas.session_schema import SessionBaseSchema


class SessionService:
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def get_all_sessions(self) -> List[SessionModel]:
        return self.repository.get_all()

    def get_session_by_id(self, session_id: int) -> SessionModel:
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with id {session_id} not found"
            )
        return session

    def create_session(self, session_data: SessionBaseSchema) -> SessionModel:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session_dict = session_data.model_dump()
        session_dict.update({
            "create_at": now,
            "update_at": now
        })
        new_session = SessionModel(**session_dict)
        return self.repository.create(new_session)

    def update_session(self, session_id: int, session_data: SessionBaseSchema) -> SessionModel:
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with id {session_id} not found"
            )
        update_data = session_data.model_dump(exclude_unset=True)
        update_data["update_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.repository.update(session_id, update_data)

    def delete_session(self, session_id: int):
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with id {session_id} not found"
            )
        self.repository.delete(session)
