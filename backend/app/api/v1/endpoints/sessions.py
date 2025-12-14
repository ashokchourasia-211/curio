from fastapi import APIRouter, HTTPException

from app.db.database import SessionDep
from app.schemas.session import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionVerifyResponse,
)
from app.services import session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionCreateResponse, status_code=201)
def create_session(
    request: SessionCreateRequest,
    db: SessionDep,
) -> SessionCreateResponse:
    """Create a new classroom session."""
    session = session_service.create_session(
        db=db,
        teacher_id=request.teacher_id,
        subject=request.subject,
    )
    return SessionCreateResponse(
        session_id=session.id,
        code=session.code,
    )


@router.get("/verify/{code}", response_model=SessionVerifyResponse)
def verify_session(
    code: str,
    db: SessionDep,
) -> SessionVerifyResponse:
    """Verify a session code exists and is active."""
    session = session_service.verify_session(db=db, code=code)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or inactive")

    return SessionVerifyResponse(
        valid=True,
        session_id=session.id,
        subject=session.subject,
    )
