from sqlalchemy import Column, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from app.database.database import Base


class MovieImagesModel(Base):
    __tablename__ = 'movie_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    poster_image_data = Column(LargeBinary, nullable=False)
    backdrop_image_data = Column(LargeBinary, nullable=False)

    movie = relationship("MovieModel", back_populates="images")