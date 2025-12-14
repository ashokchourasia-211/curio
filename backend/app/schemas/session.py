import uuid
from pydantic import BaseModel


class SessionCreateRequest(BaseModel):
    """Request body for creating a new session."""

    teacher_id: str
    subject: str


class SessionCreateResponse(BaseModel):
    """Response after creating a session."""

    session_id: uuid.UUID
    code: str


class SessionVerifyResponse(BaseModel):
    """Response when verifying a session code."""

    valid: bool
    session_id: uuid.UUID
    subject: str
