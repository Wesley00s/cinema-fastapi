from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError

from app.dependencies.session_dependencies import get_session_service
from ..schemas.session_schema import SessionBaseSchema
from ..service.session_service import SessionService

router = APIRouter()


@router.get('/session/all')
def get_sessions(service: SessionService = Depends(get_session_service)):
    try:
        sessions = service.get_all_sessions()
        return {'status': 'success', 'results': len(sessions), 'sessions': sessions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.post('/session', status_code=status.HTTP_201_CREATED)
def create_session(
        payload: SessionBaseSchema,
        service: SessionService = Depends(get_session_service)
):
    try:
        new_session = service.create_session(payload)
        return {"status": "success", "session": new_session}
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


@router.get('/session/{session_id}')
def get_session(
        session_id: int,
        service: SessionService = Depends(get_session_service)
):
    try:
        session = service.get_session_by_id(session_id)
        return {"status": "success", "session": session}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )


@router.patch('/session/{session_id}')
def update_session(
        session_id: int,
        payload: SessionBaseSchema,
        service: SessionService = Depends(get_session_service)
):
    try:
        updated_session = service.update_session(session_id, payload)
        return {"status": "success", "session": updated_session}
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


@router.delete('/session/{session_id}')
def delete_session(
        session_id: int,
        service: SessionService = Depends(get_session_service)
):
    try:
        service.delete_session(session_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred. {e}'
        )
