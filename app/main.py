import uvicorn
from starlette.responses import HTMLResponse

from app.routes import admin, customer, movie, session, room, ticket
from app import models
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/home-admin', tags=['Home'], response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home-admin.html", {"request": request})

@app.get('/home-customer', tags=['Home'], response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home-customer.html", {"request": request})

@app.get('/login-admin', tags=['Login'], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login-admin.html", {"request": request})

@app.get('/login-customer', tags=['Login'], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login-customer.html", {"request": request})

@app.get('/register-admin', tags=['Register'], response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register-admin.html", {"request": request})

@app.get('/register-customer', tags=['Register'], response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register-customer.html", {"request": request})

@app.get('/movies', tags=['Movies'], response_class=HTMLResponse)
async def movies(request: Request):
    return templates.TemplateResponse("movies.html", {"request": request})

@app.get('/rooms', tags=['Room'], response_class=HTMLResponse)
async def movies(request: Request):
    return templates.TemplateResponse("rooms.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)