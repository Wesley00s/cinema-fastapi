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

@router.post('/customer/image', status_code=status.HTTP_200_OK)
def upload_customer_image(payload: schemas.CustomerImageSchema, db: Session = Depends(get_db)):
    try:
        customer_uuid = UUID(payload.customer_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="customer_id inválido."
        )

    customer = db.query(models.Customer).filter(models.Customer.id == customer_uuid).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer com id {payload.customer_id} não encontrado."
        )

    try:
        image_str = payload.image_data
        if image_str.startswith("data:"):
            _, image_data = image_str.split(",", 1)
        else:
            image_data = image_str

        decoded_image = base64.b64decode(image_data)

        new_image = models.CustomerImage(customer_id=customer_uuid, image_data=decoded_image)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {
            "status": "success",
            "message": "Imagem carregada com sucesso.",
            "image_id": new_image.id,
            "customer_id": payload.customer_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar a imagem: {e}"
        )


@router.get('/customer/{customer_id}/image', response_class=Response)
def get_customer_image(customer_id: UUID, db: Session = Depends(get_db)):

    customer_image = db.query(models.CustomerImage).filter(models.CustomerImage.customer_id == customer_id).first()

    if not customer_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem para o customer com id {customer_id} não encontrada."
        )

    return Response(content=customer_image.image_data, media_type="image/jpeg")



@router.get('/customer/all')
def get_customers(db: Session = Depends(get_db)):
    try:
        customers = db.query(models.Customer).all()
        return {'status': 'success', 'results': len(customers), 'customers': customers}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )

@router.post('/customer', status_code=status.HTTP_201_CREATED)
def create_customer(payload: schemas.CustomerBaseSchema, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt())
    payload.password = hashed_password.decode('utf-8')

    new_customer = models.Customer(**payload.model_dump())
    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_customer.email, "id": str(new_customer.id)},
            expires_delta=access_token_expires
        )

        return {
            "status": "success",
            "customer": new_customer,
            "access_token": access_token,
            "token_type": "bearer"
        }

        return {"status": "success", "customer": new_customer}
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


@router.get('/customer')
def get_customer(id: UUID, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No customer with this id: {id} found")
    return {"status": "success", "customer": customer}


@router.get('/customer/email')
def get_customer(email: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No customer with this email: {email} found")
    return {"status": "success", "customer": customer}


@router.patch('/customer')
def update_customer(id: UUID, payload: schemas.CustomerBaseSchema, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == id)
    db_customer = customer_query.first()

    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No customer with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    customer_query.update(update_data, synchronize_session=False)
    try:
        db.commit()
        db.refresh(db_customer)
        return {"status": "success", "customer": db_customer}
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


@router.patch('/customer/reset-password')
def reset_password(payload: schemas.ResetPasswordSchema, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.email == payload.email).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    hashed_password = bcrypt.hashpw(payload.new_password.encode('utf-8'), bcrypt.gensalt())
    customer.password = hashed_password.decode('utf-8')

    db.commit()
    db.refresh(customer)

    return {"status": "success", "message": "Password updated successfully"}



@router.delete('/customer')
def delete_customer(id: UUID, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No customer with this id: {id} found')
    customer_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/customer/auth')
def auth_customer(
    payload: AuthModel,
    db: Session = Depends(get_db),
    response: Response = None
):
    customer = db.query(models.Customer).filter(models.Customer.email == payload.email).first()
    if not customer or not bcrypt.checkpw(payload.password.encode('utf-8'), customer.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": customer.email, "id": str(customer.id)},
        expires_delta=access_token_expires
    )

    response.headers["Authorization"] = f"Bearer {access_token}"

    return {"access_token": access_token, "token_type": "bearer"}
