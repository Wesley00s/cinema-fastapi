import base64
from datetime import timedelta
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.AuthModel import AuthModel
from .. import models, schemas
from ..config import settings
from ..database import get_db
from ..security import create_access_token

router = APIRouter()


@router.post('/admin/image', status_code=status.HTTP_200_OK)
def upload_admin_image(payload: schemas.AdminImageSchema, db: Session = Depends(get_db)):
    try:
        admin_uuid = UUID(payload.admin_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin_id inválido."
        )

    admin = db.query(models.Admin).filter(models.Admin.id == admin_uuid).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin com id {payload.admin_id} não encontrado."
        )

    try:
        image_str = payload.image_data
        if image_str.startswith("data:"):
            _, image_data = image_str.split(",", 1)
        else:
            image_data = image_str

        decoded_image = base64.b64decode(image_data)

        new_image = models.AdminImage(admin_id=admin_uuid, image_data=decoded_image)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {
            "status": "success",
            "message": "Imagem carregada com sucesso.",
            "image_id": new_image.id,
            "admin_id": payload.admin_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar a imagem: {e}"
        )


@router.get('/admin/{admin_id}/image', response_class=Response)
def get_admin_image(admin_id: UUID, db: Session = Depends(get_db)):
    admin_image = db.query(models.AdminImage).filter(models.AdminImage.admin_id == admin_id).first()

    if not admin_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem para o admin com id {admin_id} não encontrada."
        )

    return Response(content=admin_image.image_data, media_type="image/jpeg")


@router.get('/admin/all')
def get_admins(db: Session = Depends(get_db)):
    try:
        admins = db.query(models.Admin).all()
        return {'status': 'success', 'results': len(admins), 'admins': admins}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.post('/admin', status_code=status.HTTP_201_CREATED)
def create_admin(payload: schemas.AdminBaseSchema, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt())
    payload.password = hashed_password.decode('utf-8')

    new_admin = models.Admin(**payload.model_dump())
    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_admin.email, "id": str(new_admin.id)},
            expires_delta=access_token_expires
        )

        return {
            "status": "success",
            "admin": new_admin,
            "access_token": access_token,
            "token_type": "bearer"
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A database integrity error occurred. Please verify your data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.get('/admin')
def get_admin(id: UUID, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admin with this id: {id} found")
    return {"status": "success", "admin": admin}


@router.get('/admin/email')
def get_admin(email: str, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admin with this email: {email} found")
    return {"status": "success", "admin": admin}


@router.patch('/admin')
def update_admin(id: UUID, payload: schemas.AdminBaseSchema, db: Session = Depends(get_db)):
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)
    db_admin = admin_query.first()

    if not db_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No admin with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    admin_query.update(update_data, synchronize_session=False)
    try:
        db.commit()
        db.refresh(db_admin)
        return {"status": "success", "admin": db_admin}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A database integrity error occurred. Please verify your data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.patch('/admin/reset-password')
def reset_password(payload: schemas.ResetPasswordSchema, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == payload.email).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    hashed_password = bcrypt.hashpw(payload.new_password.encode('utf-8'), bcrypt.gensalt())
    admin.password = hashed_password.decode('utf-8')

    db.commit()
    db.refresh(admin)

    return {"status": "success", "message": "Password updated successfully"}


@router.delete('/admin')
def delete_admin(id: UUID, db: Session = Depends(get_db)):
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)
    admin = admin_query.first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No admin with this id: {id} found')
    admin_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/admin/auth')
def auth_admin(
        payload: AuthModel,
        db: Session = Depends(get_db),
        response: Response = None
):
    admin = db.query(models.Admin).filter(models.Admin.email == payload.email).first()
    if not admin or not bcrypt.checkpw(payload.password.encode('utf-8'), admin.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email, "id": str(admin.id)},
        expires_delta=access_token_expires
    )

    response.headers["Authorization"] = f"Bearer {access_token}"

    return {"access_token": access_token, "token_type": "bearer"}
