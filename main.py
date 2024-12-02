from fastapi import FastAPI
import uvicorn

from database.Database import Database
from repository.AdminRepository import AdminRepository
from repository.CustomerRepository import CustomerRepository
from service.AdminService import AdminService
from service.CustomerService import CustomerService

app = FastAPI()

customer_repository = CustomerRepository()
customer_service = CustomerService(customer_repository)

admin_repository = AdminRepository()
admin_service = AdminService(admin_repository)

app.add_api_route("/customer", customer_service.create, methods=["POST"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.get_by_id, methods=["GET"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.update, methods=["PUT"], tags=['Customer'])
app.add_api_route("/customer/{id}", customer_service.delete, methods=["DELETE"], tags=['Customer'])
app.add_api_route("/customer/auth", customer_service.auth, methods=["POST"], tags=['Customer'])

app.add_api_route("/admin", admin_service.create, methods=["POST"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.get_by_id, methods=["GET"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.update, methods=["PUT"], tags=['Admin'])
app.add_api_route("/admin/{id}", admin_service.delete, methods=["DELETE"], tags=['Admin'])
app.add_api_route("/admin/auth", admin_service.auth, methods=["POST"], tags=['Admin'])

if __name__ == '__main__':
    Database.create_all_tables()
    uvicorn.run(app, host='0.0.0.0', port=8000)