import uuid
from sqlmodel import Field, SQLModel


class Session(SQLModel, table=True):  # type: ignore[call-arg]
    """Classroom session created by a teacher."""

    __tablename__ = "sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str = Field(max_length=6, unique=True, index=True)
    subject: str
    teacher_id: str
    is_active: bool = Field(default=True)
