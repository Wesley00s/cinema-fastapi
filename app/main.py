import uvicorn

from app.routes import admin, customer, movie, session, room, ticket
from app import models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, tags=['Admin'])
app.include_router(customer.router, tags=['Customer'])
app.include_router(movie.router, tags=['Movie'])
app.include_router(session.router, tags=['Session'])
app.include_router(room.router, tags=['Room'])
app.include_router(ticket.router, tags=['Ticket'])

@app.get('/', tags=['Root'])
def root():
    return {'status': 'success', 'message': 'Cinema API say hello 👋'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)