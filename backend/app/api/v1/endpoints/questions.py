import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.db.database import SessionDep
from app.schemas.question import QuestionCreateRequest, QuestionResponse, QuestionStatus
from app.services import question_service

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("", response_model=QuestionResponse)
def post_question(
    request: QuestionCreateRequest,
    db: SessionDep,
) -> QuestionResponse:
    """Post a new question and get AI response."""
    try:
        question, status = question_service.create_question(
            db=db,
            session_id=request.session_id,
            text=request.text,
            student_hash=request.student_hash,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return QuestionResponse(
        question_id=question.id,
        text=question.text,
        student_name=question.student_name,
        ai_response=question.ai_response,
        status=status,
        created_at=question.created_at,
    )


@router.get("/{session_id}", response_model=list[QuestionResponse])
def get_questions(
    session_id: uuid.UUID,
    db: SessionDep,
    last_seen_timestamp: datetime | None = Query(default=None),
) -> list[QuestionResponse]:
    """Get questions for a session (polling endpoint)."""
    questions = question_service.get_questions(
        db=db,
        session_id=session_id,
        last_seen_timestamp=last_seen_timestamp,
    )

    return [
        QuestionResponse(
            question_id=q.id,
            text=q.text,
            student_name=q.student_name,
            ai_response=q.ai_response,
            status=QuestionStatus.FLAGGED if q.is_flagged else QuestionStatus.POSTED,
            created_at=q.created_at,
        )
        for q in questions
    ]
