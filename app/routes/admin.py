from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.dependencies.admin_dependencies import get_admin_service
from app.models.auth_model import AuthModel
from app.schemas.admin_image_schema import AdminImageSchema
from app.schemas.admin_schema import AdminBaseSchema
from app.schemas.reset_password_schema import ResetPasswordSchema
from app.service.admin_service import AdminService

router = APIRouter()


@router.post('/admin/image', status_code=status.HTTP_200_OK)
def upload_admin_image(
        payload: AdminImageSchema,
        service: AdminService = Depends(get_admin_service)
):
    try:
        image = service.upload_image(payload)
        return {
            "status": "success",
            "message": "Image has been uploaded successfully",
            "image_id": image.id,
            "admin_id": payload.admin_id
        }
    except HTTPException as e:
        raise e


@router.get('/admin/{admin_id}/image', response_class=Response)
def get_admin_image(
        admin_id: UUID,
        service: AdminService = Depends(get_admin_service)
):
    try:
        image_data = service.get_admin_image(admin_id)
        return Response(content=image_data, media_type="image/jpeg")
    except HTTPException as e:
        raise e


@router.get('/admin/all')
def get_admins(service: AdminService = Depends(get_admin_service)):
    return {'status': 'success', 'admins': service.get_all_admins()}


@router.post('/admin', status_code=status.HTTP_201_CREATED)
def create_admin(
        payload: AdminBaseSchema,
        service: AdminService = Depends(get_admin_service)
):
    try:
        result = service.create_admin(payload)
        return {
            "status": "success",
            "admin": result["admin"],
            "access_token": result["access_token"],
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e


@router.get('/admin/{admin_id}')
def get_admin(
        admin_id: UUID,
        service: AdminService = Depends(get_admin_service)
):
    return {"status": "success", "admin": service.get_admin_by_id(admin_id)}


@router.get('/admin/email/{admin_email}')
def get_admin_by_email(
        admin_email: str,
        service: AdminService = Depends(get_admin_service)
):
    return {"status": "success", "admin": service.get_admin_by_email(admin_email)}


@router.patch('/admin/{admin_id}')
def update_admin(
        admin_id: UUID,
        payload: AdminBaseSchema,
        service: AdminService = Depends(get_admin_service)
):
    try:
        result = service.update_admin(admin_id, payload)
        return {"status": "success", "admin": result}
    except HTTPException as e:
        raise e


@router.patch('/admin/reset-password')
def reset_password(
        payload: ResetPasswordSchema,
        service: AdminService = Depends(get_admin_service)
):
    try:
        result = service.reset_password(payload)
        return {
            "status": "success",
        }
    except HTTPException as e:
        raise e


@router.delete('/admin/{admin_id}')
def delete_admin(
        admin_id: UUID,
        service: AdminService = Depends(get_admin_service)
):
    try:
        result = service.delete_admin(admin_id)
        return {
            "status": "success",
        }
    except HTTPException as e:
        raise e


@router.post('/admin/auth')
def auth_admin(
        payload: AuthModel,
        service: AdminService = Depends(get_admin_service),
        response: Response = None
):
    try:
        token = service.authenticate_admin(payload)
        response.headers["Authorization"] = f"Bearer {token}"
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
