import uuid

from app.database import Base
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Boolean, UUID


class User(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)


class Customer(User):
    __tablename__ = 'customer'
    age = Column(Integer, nullable=True)


class Admin(User):
    __tablename__ = 'admin'
    pass


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    synopsis = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    age_rating = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    language = Column(String, nullable=False)
    subtitles = Column(Boolean, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    customer_id = Column(UUID, ForeignKey('customer.id'), nullable=False)
    seat_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
