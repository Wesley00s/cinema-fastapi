from datetime import datetime

from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()



@router.get('/ticket/all')
def get_tickets(db: Session = Depends(get_db)):
    try:
        tickets = db.query(models.Ticket).all()
        return {'status': 'success', 'results': len(tickets), 'tickets': tickets}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )

@router.post('/ticket', status_code=status.HTTP_201_CREATED)
def create_ticket(payload: schemas.TicketBaseSchema, db: Session = Depends(get_db)):
    new_ticket = models.Ticket(**payload.model_dump())
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_ticket.create_at = now
        new_ticket.update_at = now
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return {"status": "success", "ticket": new_ticket}
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


@router.get('/ticket/')
def get_ticket(id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No ticket with this id: {id} found")
    return {"status": "success", "ticket": ticket}


@router.patch('/ticket/')
def update_ticket(id: int, payload: schemas.TicketBaseSchema, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == id)
    db_ticket = ticket_query.first()

    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ticket with this id: {id} found')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_ticket.update_at = now
    update_data = payload.model_dump(exclude_unset=True)
    ticket_query.update(update_data, synchronize_session=False)
    try:
        db.commit()
        db.refresh(db_ticket)
        return {"status": "success", "ticket": db_ticket}
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


@router.delete('/ticket/')
def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == id)
    ticket = ticket_query.first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ticket with this id: {id} found')
    ticket_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
