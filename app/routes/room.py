from datetime import datetime

from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()



@router.get('/room')
def get_rooms(db: Session = Depends(get_db)):
    try:
        rooms = db.query(models.Room).all()
        return {'status': 'success', 'results': len(rooms), 'rooms': rooms}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )

@router.post('/room', status_code=status.HTTP_201_CREATED)
def create_room(payload: schemas.RoomBaseSchema, db: Session = Depends(get_db)):
    new_room = models.Room(**payload.model_dump())
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_room.create_at = now
        new_room.update_at = now
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return {"status": "success", "room": new_room}
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


@router.get('/room')
def get_room(id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No room with this id: {id} found")
    return {"status": "success", "room": room}


@router.patch('/room')
def update_room(id: int, payload: schemas.RoomBaseSchema, db: Session = Depends(get_db)):
    room_query = db.query(models.Room).filter(models.Room.id == id)
    db_room = room_query.first()

    if not db_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No room with this id: {id} found')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_room.update_at = now
    update_data = payload.model_dump(exclude_unset=True)
    room_query.update(update_data, synchronize_session=False)
    try:
        db.commit()
        db.refresh(db_room)
        return {"status": "success", "room": db_room}
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


@router.delete('/room')
def delete_room(id: int, db: Session = Depends(get_db)):
    room_query = db.query(models.Room).filter(models.Room.id == id)
    room = room_query.first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No room with this id: {id} found')
    room_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
