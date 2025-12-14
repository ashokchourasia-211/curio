import uuid
from datetime import datetime
from pydantic import BaseModel


class QuestionGroupResponse(BaseModel):
    """Response model for a question group."""

    id: uuid.UUID
    session_id: uuid.UUID
    topic: str
    created_at: datetime
    question_count: int


class GroupAnswerRequest(BaseModel):
    """Request model for answering a group of questions."""

    answer: str
