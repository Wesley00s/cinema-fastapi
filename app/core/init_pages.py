from fastapi import APIRouter, Request, FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

router = APIRouter(tags=['Pages'])
templates = Jinja2Templates(directory="app/templates")


def init_pages(app: FastAPI):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/", tags=['Page'], response_class=HTMLResponse)
    async def root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get('/home-admin', tags=['Page'], response_class=HTMLResponse)
    async def home(request: Request):
        return templates.TemplateResponse("home-admin.html", {"request": request})

    @app.get('/login-admin', tags=['Page'], response_class=HTMLResponse)
    async def login(request: Request):
        return templates.TemplateResponse("login-admin.html", {"request": request})

    @app.get('/login-customer', tags=['Page'], response_class=HTMLResponse)
    async def login(request: Request):
        return templates.TemplateResponse("login-customer.html", {"request": request})

    @app.get('/register-admin', tags=['Page'], response_class=HTMLResponse)
    async def register(request: Request):
        return templates.TemplateResponse("register-admin.html", {"request": request})

    @app.get('/register-customer', tags=['Page'], response_class=HTMLResponse)
    async def register(request: Request):
        return templates.TemplateResponse("register-customer.html", {"request": request})

    @app.get('/movies', tags=['Page'], response_class=HTMLResponse)
    async def movies(request: Request):
        return templates.TemplateResponse("movies.html", {"request": request})

    @app.get('/rooms', tags=['Page'], response_class=HTMLResponse)
    async def rooms(request: Request):
        return templates.TemplateResponse("rooms.html", {"request": request})

    @app.get('/sessions', tags=['Page'], response_class=HTMLResponse)
    async def sessions(request: Request):
        return templates.TemplateResponse("session.html", {"request": request})

    @app.get('/session-customer', tags=['Page'], response_class=HTMLResponse)
    async def session_customer(request: Request):
        return templates.TemplateResponse("session-customer.html", {"request": request})

    @app.get('/tickets', tags=['Page'], response_class=HTMLResponse)
    async def tickets(request: Request):
        return templates.TemplateResponse("ticket.html", {"request": request})

    @app.get('/profile-admin', tags=['Page'], response_class=HTMLResponse)
    async def profile_admin(request: Request):
        return templates.TemplateResponse("profile-admin.html", {"request": request})

    @app.get('/profile-customer', tags=['Page'], response_class=HTMLResponse)
    async def profile_customer(request: Request):
        return templates.TemplateResponse("profile-customer.html", {"request": request})

    @app.get('/recovery-password-admin', tags=['Page'], response_class=HTMLResponse)
    async def recovery_password_admin(request: Request):
        return templates.TemplateResponse("recovery-password-admin.html", {"request": request})

    @app.get('/recovery-password-customer', tags=['Page'], response_class=HTMLResponse)
    async def recovery_password_customer(request: Request):
        return templates.TemplateResponse("recovery-password-customer.html", {"request": request})

    @app.get('/session-details/{session_id}', tags=['Page'], response_class=HTMLResponse)
    async def session_details(request: Request, session_id: int):
        return templates.TemplateResponse("session-details.html", {"request": request, "session_id": session_id})