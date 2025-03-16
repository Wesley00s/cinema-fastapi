from sqlalchemy import Column, Integer, ForeignKey, UUID, LargeBinary

from app.database.database import Base


class AdminImageModel(Base):
    __tablename__ = 'admin_image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey('admin.id'), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
