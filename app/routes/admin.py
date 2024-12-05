from math import trunc
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.AuthModel import AuthModel
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/admin')
def get_admins(db: Session = Depends(get_db)):
    try:
        admins = db.query(models.Admin).all()
        return {'status': 'success', 'results': len(admins), 'admins': admins}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
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
        return {"status": "success", "admin": new_admin}
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
            detail="An unexpected error occurred."
        )


@router.get('/admin/{id}')
def get_admin(id: UUID, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admin with this id: {id} found")
    return {"status": "success", "admin": admin}


@router.patch('/admin/{id}')
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
            detail="An unexpected error occurred."
        )


@router.delete('/admin/{id}')
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
def auth_admin(payload: AuthModel, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == payload.email).first()
    if not admin or not bcrypt.checkpw(payload.password.encode('utf-8'), admin.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"status": "success", "admin": admin}
