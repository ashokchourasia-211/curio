import random
import string
import uuid
from typing import cast

from sqlmodel import Session, select

from app.models.session import Session as SessionModel


def generate_code() -> str:
    """Generate a unique 6-char session code like 'ABC-12'."""
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    digits = "".join(random.choices(string.digits, k=2))
    return f"{letters}-{digits}"


def create_session(
    db: Session,
    teacher_id: str,
    subject: str,
) -> SessionModel:
    """Create a new classroom session with a unique code."""
    # Generate a unique code (retry if collision)
    for _ in range(10):
        code = generate_code()
        existing = db.exec(
            select(SessionModel).where(SessionModel.code == code)
        ).first()
        if not existing:
            break
    else:
        # Fallback to UUID-based code if all retries fail
        code = str(uuid.uuid4())[:6].upper()

    session = SessionModel(
        teacher_id=teacher_id,
        subject=subject,
        code=code,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def verify_session(db: Session, code: str) -> SessionModel | None:
    """Verify a session code exists and is active."""
    session = db.exec(
        select(SessionModel).where(
            SessionModel.code == code,
            SessionModel.is_active == True,  # noqa: E712
        )
    ).first()
    return cast(SessionModel | None, session)


def get_session_by_id(db: Session, session_id: uuid.UUID) -> SessionModel | None:
    """Get a session by its ID."""
    return cast(SessionModel | None, db.get(SessionModel, session_id))
