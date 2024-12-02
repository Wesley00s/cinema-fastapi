from fastapi import FastAPI
import uvicorn

from database.Database import Database
from repository.AdminRepository import AdminRepository
from repository.CustomerRepository import CustomerRepository
from repository.MovieRepository import MovieRepository
from repository.RoomRepository import RoomRepository
from repository.SessionRepository import SessionRepository
from repository.TicketRepository import TicketRepository
from service.AdminService import AdminService
from service.CustomerService import CustomerService
from service.MovieService import MovieService
from service.RoomService import RoomService
from service.SessionService import SessionService
from service.TicketService import TicketService

app = FastAPI()

customer_repository = CustomerRepository()
customer_service = CustomerService(customer_repository)

admin_repository = AdminRepository()
admin_service = AdminService(admin_repository)

movie_repository = MovieRepository()
movie_service = MovieService(movie_repository)

room_repository = RoomRepository()
room_service = RoomService(room_repository)

session_repository = SessionRepository()
session_service = SessionService(
    session_repository,
    room_repository,
    movie_repository
)

ticket_repository = TicketRepository()
ticket_service = TicketService(
    ticket_repository,
    session_repository,
    customer_repository
)

app.add_api_route("/customer", customer_service.create, methods=["POST"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.get_by_id, methods=["GET"], tags=['Customer'])
app.add_api_route("/customer", customer_service.get_all, methods=["GET"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.update, methods=["PUT"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.delete, methods=["DELETE"], tags=['Customer'])
app.add_api_route("/customer/auth", customer_service.auth, methods=["POST"], tags=['Customer'])

app.add_api_route("/admin", admin_service.create, methods=["POST"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.get_by_id, methods=["GET"], tags=['Admin'])
app.add_api_route("/admin", admin_service.get_all, methods=["GET"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.update, methods=["PUT"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.delete, methods=["DELETE"], tags=['Admin'])
app.add_api_route("/admin/auth", admin_service.auth, methods=["POST"], tags=['Admin'])

app.add_api_route("/movie", movie_service.create, methods=["POST"], tags=['Movie'])
app.add_api_route("/movie/{id}", movie_service.get_by_id, methods=["GET"], tags=['Movie'])
app.add_api_route("/movie", movie_service.get_all, methods=["GET"], tags=['Movie'])
app.add_api_route("/movie/{id}", movie_service.update, methods=["PUT"], tags=['Movie'])
app.add_api_route("/movie/{id}", movie_service.delete, methods=["DELETE"], tags=['Movie'])

app.add_api_route("/room", room_service.create, methods=["POST"], tags=['Room'])
app.add_api_route("/room/{id}", room_service.get_by_id, methods=["GET"], tags=['Room'])
app.add_api_route("/room", room_service.get_all, methods=["GET"], tags=['Room'])
app.add_api_route("/room/{id}", room_service.update, methods=["PUT"], tags=['Room'])
app.add_api_route("/room/{id}", room_service.delete, methods=["DELETE"], tags=['Room'])

app.add_api_route("/session", session_service.create, methods=["POST"], tags=['Session'])
app.add_api_route("/session/{id}", session_service.get_by_id, methods=["GET"], tags=['Session'])
app.add_api_route("/session", session_service.get_all, methods=["GET"], tags=['Session'])
app.add_api_route("/session/{id}", session_service.update, methods=["PUT"], tags=['Session'])
app.add_api_route("/session/{id}", session_service.delete, methods=["DELETE"], tags=['Session'])

app.add_api_route("/ticket", ticket_service.create, methods=["POST"], tags=['Ticket'])
app.add_api_route("/ticket/{id}", ticket_service.get_by_id, methods=["GET"], tags=['Ticket'])
app.add_api_route("/ticket", ticket_service.get_all, methods=["GET"], tags=['Ticket'])
app.add_api_route("/ticket/{id}", ticket_service.update, methods=["PUT"], tags=['Ticket'])
app.add_api_route("/ticket/{id}", ticket_service.delete, methods=["DELETE"], tags=['Ticket'])

if __name__ == '__main__':
    Database.create_all_tables()
    uvicorn.run(app, host='0.0.0.0', port=8000)