from sqlalchemy import Column, Integer, ForeignKey, UUID, LargeBinary

from app.database.database import Base


class MovieImageModel(Base):
    __tablename__ = 'movie_image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
