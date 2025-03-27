from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.dependencies.customer_dependencies import get_customer_service
from app.models.auth_model import AuthModel
from app.schemas.customer_image_schema import CustomerImageSchema
from app.schemas.customer_schema import CustomerBaseSchema
from app.schemas.reset_password_schema import ResetPasswordSchema
from app.service.customer_service import CustomerService

router = APIRouter()


@router.post('/customer/image', status_code=status.HTTP_200_OK)
def upload_customer_image(
        payload: CustomerImageSchema,
        service: CustomerService = Depends(get_customer_service)
):
    try:
        image = service.upload_image(payload)
        return {
            "status": "success",
            "message": "Image has been uploaded successfully",
            "image_id": image.id,
            "customer_id": payload.customer_id
        }
    except HTTPException as e:
        raise e


@router.get('/customer/{customer_id}/image', response_class=Response)
def get_customer_image(
        customer_id: UUID,
        service: CustomerService = Depends(get_customer_service)
):
    try:
        image_data = service.get_customer_image(customer_id)
        return Response(content=image_data, media_type="image/jpeg")
    except HTTPException as e:
        raise e


@router.get('/customer/all')
def get_customers(service: CustomerService = Depends(get_customer_service)):
    return {'status': 'success', 'customers': service.get_all_customers()}


@router.post('/customer', status_code=status.HTTP_201_CREATED)
def create_customer(
        payload: CustomerBaseSchema,
        service: CustomerService = Depends(get_customer_service)
):
    result = service.create_customer(payload)
    return {
        "status": "success",
        "customer": result["customer"],
        "access_token": result["access_token"],
        "token_type": "bearer"
    }


@router.get('/customer/{customer_id}')
def get_customer(
        customer_id: UUID,
        service: CustomerService = Depends(get_customer_service)
):
    return {"status": "success", "customer": service.get_customer_by_id(customer_id)}


@router.get('/customer/email/{customer_email}')
def get_customer_by_email(
        customer_email: str,
        service: CustomerService = Depends(get_customer_service)
):
    return {"status": "success", "customer": service.get_customer_by_email(customer_email)}


@router.patch('/customer/reset-password')
def reset_password(
        payload: ResetPasswordSchema,
        service: CustomerService = Depends(get_customer_service)
):
    service.reset_password(payload)
    return {"status": "success", "message": "Senha atualizada com sucesso"}


@router.patch('/customer/{customer_id}')
def update_customer(
        customer_id: UUID,
        payload: CustomerBaseSchema,
        service: CustomerService = Depends(get_customer_service)
):
    return {"status": "success", "customer": service.update_customer(customer_id, payload)}


@router.delete('/customer/{customer_id}')
def delete_customer(
        customer_id: UUID,
        service: CustomerService = Depends(get_customer_service)
):
    service.delete_customer(customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/customer/auth')
def auth_customer(
        payload: AuthModel,
        service: CustomerService = Depends(get_customer_service),
        response: Response = None
):
    token = service.authenticate_customer(payload)
    response.headers["Authorization"] = f"Bearer {token}"
    return {"access_token": token, "token_type": "bearer"}
