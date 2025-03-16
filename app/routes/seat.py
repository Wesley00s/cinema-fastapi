from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError

from app.dependencies.seat_dependencies import get_seat_service
from ..schemas.seat_schema import SeatBaseSchema
from ..service.seat_service import SeatService

router = APIRouter()


@router.get('/seat/all')
def get_seats(service: SeatService = Depends(get_seat_service)):
    try:
        seats = service.get_all_seats()
        return {'status': 'success', 'results': len(seats), 'seats': seats}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.get('/seat/{seat_id}')
def get_seat(
        seat_id: int,
        service: SeatService = Depends(get_seat_service)
):
    try:
        seat = service.get_seat_by_id(seat_id)
        return {"status": "success", "seat": seat}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.get('/seat/room/{room_id}')
def get_seats_room(
        room_id: int,
        service: SeatService = Depends(get_seat_service)
):
    try:
        seats = service.get_seats_by_room_id(room_id)
        return {"status": "success",'results': len(seats), "seats": seats}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.patch('/seat/{seat_id}')
def update_seat(
        seat_id: int,
        payload: SeatBaseSchema,
        service: SeatService = Depends(get_seat_service)
):
    try:
        updated_seat = service.update_seat(seat_id, payload)
        return {"status": "success", "seat": updated_seat}
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
            detail="An unexpected error occurred."
        )


@router.delete('/seat/{seat_id}')
def delete_seat(
        seat_id: int,
        service: SeatService = Depends(get_seat_service)
):
    try:
        service.delete_seat(seat_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
