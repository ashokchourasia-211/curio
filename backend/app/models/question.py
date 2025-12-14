import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Question(SQLModel, table=True):  # type: ignore[call-arg]
    """Anonymous question posted by a student."""

    __tablename__ = "questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="sessions.id", index=True)
    student_hash: str
    student_name: str
    text: str
    ai_response: str | None = Field(default=None)
    is_flagged: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
