from fastapi import FastAPI

from app.routes.admin import router as admin_router
from app.routes.customer import router as customer_router
from app.routes.movie import router as movie_router
from app.routes.room import router as room_router
from app.routes.seat import router as seat_router
from app.routes.session import router as session_router
from app.routes.ticket import router as ticket_router


def init_routers(app: FastAPI):
    app.include_router(admin_router, tags=['Admin'])
    app.include_router(customer_router, tags=['Customer'])
    app.include_router(movie_router, tags=['Movie'])
    app.include_router(session_router, tags=['Session'])
    app.include_router(room_router, tags=['Room'])
    app.include_router(seat_router, tags=['Seat'])
    app.include_router(ticket_router, tags=['Ticket'])
