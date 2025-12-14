import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class QuestionStatus(str, Enum):
    """Status of a question after AI processing."""

    POSTED = "posted"
    FLAGGED = "flagged"


class QuestionCreateRequest(BaseModel):
    """Request body for posting a new question."""

    session_id: uuid.UUID
    text: str
    student_hash: str


class QuestionResponse(BaseModel):
    """Response containing question details and AI response."""

    question_id: uuid.UUID
    text: str
    student_name: str
    ai_response: str | None
    status: QuestionStatus
    created_at: datetime
