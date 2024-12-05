from datetime import datetime

from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/session')
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).all()
    return {'status': 'success', 'results': len(sessions), 'sessions': sessions}


@router.post('/session', status_code=status.HTTP_201_CREATED)
def create_session(payload: schemas.SessionBaseSchema, db: Session = Depends(get_db)):
    new_session = models.Session(**payload.model_dump())
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_session.create_at = now
    new_session.update_at = now
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"status": "success", "session": new_session}


@router.get('/session/{id}')
def get_session(id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No session with this id: {id} found")
    return {"status": "success", "session": session}


@router.patch('/session/{id}')
def update_session(id: int, payload: schemas.SessionBaseSchema, db: Session = Depends(get_db)):
    session_query = db.query(models.Session).filter(models.Session.id == id)
    db_session = session_query.first()

    if not db_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No session with this id: {id} found')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_session.update_at = now
    update_data = payload.model_dump(exclude_unset=True)
    session_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_session)
    return {"status": "success", "session": db_session}


@router.delete('/session/{id}')
def delete_session(id: int, db: Session = Depends(get_db)):
    session_query = db.query(models.Session).filter(models.Session.id == id)
    session = session_query.first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No session with this id: {id} found')
    session_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
