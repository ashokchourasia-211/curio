import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class QuestionGroup(SQLModel, table=True):  # type: ignore[call-arg]
    """A group of similar questions (smart grouping)."""

    __tablename__ = "question_groups"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="sessions.id", index=True)
    topic: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
