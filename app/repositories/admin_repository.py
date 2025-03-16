from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.admin_image_model import AdminImageModel
from app.models.admin_model import AdminModel


class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(AdminModel).all()

    def get_by_id(self, admin_id: UUID):
        return self.db.query(AdminModel).filter(AdminModel.id == admin_id).first()

    def get_by_email(self, email: str):
        return self.db.query(AdminModel).filter(AdminModel.email == email).first()

    def create(self, admin: AdminModel):
        try:
            self.db.add(admin)
            self.db.commit()
            self.db.refresh(admin)
            return admin
        except IntegrityError as e:
            self.db.rollback()
            raise e

    def update(self, admin_id: UUID, update_data: dict):
        try:
            admin_query = self.db.query(AdminModel).filter(AdminModel.id == admin_id)
            admin = admin_query.first()
            if not admin:
                return None
            admin_query.update(update_data, synchronize_session=False)
            self.db.commit()
            self.db.refresh(admin)
            return admin
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, admin: AdminModel):
        try:
            self.db.delete(admin)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def create_admin_image(self, image: AdminImageModel):
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_admin_image(self, admin_id: UUID):
        return self.db.query(AdminImageModel).filter(AdminImageModel.admin_id == admin_id).first()
