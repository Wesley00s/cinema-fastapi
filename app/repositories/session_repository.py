from sqlalchemy.orm import Session

from app.models.session_model import SessionModel


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(SessionModel).all()

    def get_by_id(self, session_id: int):
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def create(self, session: SessionModel):
        try:
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            return session
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, session_id: int, update_data: dict):
        try:
            session_query = self.db.query(SessionModel).filter(SessionModel.id == session_id)
            session = session_query.first()
            if not session:
                return None
            session_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(session)
            return session
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, session: SessionModel):
        try:
            self.db.delete(session)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
