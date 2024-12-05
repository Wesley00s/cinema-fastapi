from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.AuthModel import AuthModel
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/customer')
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


@router.get('/customer/')
def get_customer(id: UUID, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No customer with this id: {id} found")
    return {"status": "success", "customer": customer}


@router.patch('/customer/')
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
        return {"status": "success", "admin": db_customer}
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


@router.delete('/customer/')
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
def auth_customer(payload: AuthModel, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.email == payload.email).first()
    if not customer or not bcrypt.checkpw(payload.password.encode('utf-8'), customer.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"status": "success", "customer": customer}
