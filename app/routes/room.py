from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError

from app.dependencies.room_dependencies import get_room_service
from ..schemas.room_schema import RoomBaseSchema
from ..service.room_service import RoomService

router = APIRouter()


@router.get('/room/all')
def get_rooms(service: RoomService = Depends(get_room_service)):
    try:
        rooms = service.get_all_rooms()
        return {'status': 'success', 'results': len(rooms), 'rooms': rooms}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.post('/room', status_code=status.HTTP_201_CREATED)
def create_room(
        payload: RoomBaseSchema,
        service: RoomService = Depends(get_room_service)
):
    try:
        new_room = service.create_room(payload)
        return {"status": "success", "room": new_room}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A database integrity error occurred. Please verify your data."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}"
        )


@router.get('/room/{room_id}')
def get_room(
        room_id: int,
        service: RoomService = Depends(get_room_service)
):
    try:
        room = service.get_room_by_id(room_id)
        return {"status": "success", "room": room}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.patch('/room/{room_id}')
def update_room(
        room_id: int,
        payload: RoomBaseSchema,
        service: RoomService = Depends(get_room_service)
):
    try:
        updated_room = service.update_room(room_id, payload)
        return {"status": "success", "room": updated_room}
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


@router.delete('/room/{room_id}')
def delete_room(
        room_id: int,
        service: RoomService = Depends(get_room_service)
):
    try:
        service.delete_room(room_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
