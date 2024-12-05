
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/ticket')
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return {'status': 'success', 'results': len(tickets), 'tickets': tickets}


@router.post('/ticket', status_code=status.HTTP_201_CREATED)
def create_ticket(payload: schemas.TicketBaseSchema, db: Session = Depends(get_db)):
    new_ticket = models.Ticket(**payload.model_dump())

    existing_session = db.query(models.Session).filter(models.Session.id == payload.session_id).first()
    if not existing_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )

    existing_movie = db.query(models.Movie).filter(models.Movie.id == existing_session.movie_id).first()
    if not existing_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found."
        )

    existing_user = db.query(models.Customer).filter(models.Customer.id == payload.customer_id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    if existing_movie.age_rating > existing_user.age:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"You are not allowed to watch this movie. Age rating is {existing_movie.age_rating}, but your age is {existing_user.age}."
        )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {"status": "success", "ticket": new_ticket}


@router.get('/ticket/{id}')
def get_ticket(id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No ticket with this id: {id} found")
    return {"status": "success", "ticket": ticket}


@router.patch('/ticket/{id}')
def update_ticket(id: int, payload: schemas.TicketBaseSchema, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == id)
    db_ticket = ticket_query.first()

    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ticket with this id: {id} found')
    update_data = payload.model_dump(exclude_unset=True)
    ticket_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_ticket)
    return {"status": "success", "ticket": db_ticket}


@router.delete('/ticket/{id}')
def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == id)
    ticket = ticket_query.first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ticket with this id: {id} found')
    ticket_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
