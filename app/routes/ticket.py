from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError

from app.dependencies.ticket_dependencies import get_ticket_service
from ..schemas.ticket_schema import TicketBaseSchema
from ..service.ticket_service import TicketService

router = APIRouter()


@router.get('/ticket/all')
def get_tickets(service: TicketService = Depends(get_ticket_service)):
    try:
        tickets = service.get_all_tickets()
        return {'status': 'success', 'results': len(tickets), 'tickets': tickets}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.post('/ticket', status_code=status.HTTP_201_CREATED)
def create_ticket(
        payload: TicketBaseSchema,
        service: TicketService = Depends(get_ticket_service)
):
    try:
        new_ticket = service.create_ticket(payload)
        return {"status": "success", "ticket": new_ticket}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error. Check your input."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.get('/ticket/{ticket_id}')
def get_ticket(
        ticket_id: int,
        service: TicketService = Depends(get_ticket_service)
):
    try:
        ticket = service.get_ticket_by_id(ticket_id)
        return {"status": "success", "ticket": ticket}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.patch('/ticket/{ticket_id}')
def update_ticket(
        ticket_id: int,
        payload: TicketBaseSchema,
        service: TicketService = Depends(get_ticket_service)
):
    try:
        updated_ticket = service.update_ticket(ticket_id, payload)
        return {"status": "success", "ticket": updated_ticket}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error. Check your input."
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.delete('/ticket/{ticket_id}')
def delete_ticket(
        ticket_id: int,
        service: TicketService = Depends(get_ticket_service)
):
    try:
        service.delete_ticket(ticket_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )
