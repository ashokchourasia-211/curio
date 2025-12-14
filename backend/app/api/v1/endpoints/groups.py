import uuid

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.db.database import SessionDep
from app.models.group import QuestionGroup
from app.models.question import Question
from app.schemas.group import QuestionGroupResponse, GroupAnswerRequest

router = APIRouter(tags=["groups"])


@router.get("/sessions/{session_id}/groups", response_model=list[QuestionGroupResponse])
def get_session_groups(
    session_id: uuid.UUID,
    db: SessionDep,
) -> list[QuestionGroupResponse]:
    """Get all question groups for a specific session."""
    # This query fetches groups and counts the number of questions in each group
    # Note: This is an efficient way to get counts.
    # For MVP, we can also iterate or separate queries, but this is cleaner.

    # Simple approach first: get groups, then count (N+1 query issue but safe for MVP).
    # Or better: join.

    groups = db.exec(
        select(QuestionGroup).where(QuestionGroup.session_id == session_id)
    ).all()

    response = []
    for group in groups:
        count = db.exec(
            select(func.count(Question.id)).where(Question.group_id == group.id)
        ).one()

        response.append(
            QuestionGroupResponse(
                id=group.id,
                session_id=group.session_id,
                topic=group.topic,
                created_at=group.created_at,
                question_count=count,
            )
        )

    return response


@router.post("/groups/{group_id}/answer")
def answer_group(
    group_id: uuid.UUID,
    request: GroupAnswerRequest,
    db: SessionDep,
) -> dict[str, str]:
    """Answer all questions in a group with the same answer."""
    group = db.get(QuestionGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Update all questions in the group
    statement = select(Question).where(Question.group_id == group_id)
    questions = db.exec(statement).all()

    for question in questions:
        question.ai_response = request.answer
        # We might want a separate field for 'teacher_response', but reusing ai_response
        # or appending to it is fine for MVP as per requirements (teacher answers once).
        db.add(question)

    db.commit()

    return {"status": "success", "message": f"Answered {len(questions)} questions."}
