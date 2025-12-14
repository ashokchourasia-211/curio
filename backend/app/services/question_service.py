import random
import uuid
from datetime import datetime

from sqlmodel import Session, select

from app.models.question import Question
from app.schemas.question import QuestionStatus
from app.services.ai_agent_service import process_question_sync
from app.services.session_service import get_session_by_id

# Word lists for random name generation
ADJECTIVES = [
    "Anonymous",
    "Mysterious",
    "Curious",
    "Clever",
    "Bright",
    "Quick",
    "Silent",
    "Wise",
    "Gentle",
    "Bold",
]

ANIMALS = [
    "Panda",
    "Tiger",
    "Owl",
    "Fox",
    "Eagle",
    "Dolphin",
    "Wolf",
    "Hawk",
    "Bear",
    "Falcon",
]


def generate_display_name() -> str:
    """Generate a random display name like 'Anonymous Panda'."""
    adjective = random.choice(ADJECTIVES)
    animal = random.choice(ANIMALS)
    return f"{adjective} {animal}"


def create_question(
    db: Session,
    session_id: uuid.UUID,
    text: str,
    student_hash: str,
) -> tuple[Question, QuestionStatus]:
    """Create a new question, process through AI, and persist."""
    # Verify session exists
    session = get_session_by_id(db, session_id)
    if not session or not session.is_active:
        raise ValueError("Session not found or inactive")

    # Process through AI agent
    ai_response = process_question_sync(text)

    # Smart Grouping Logic
    from app.services.embedding import generate_embedding
    from app.services.grouping import find_or_create_group

    embedding = []
    group_id = None

    if not ai_response.is_flagged:
        try:
            embedding = generate_embedding(text)
            if embedding:
                group_id = find_or_create_group(
                    db=db,
                    session_id=session_id,
                    new_question_text=text,
                    new_embedding=embedding,
                )
        except Exception as e:
            # Fallback gracefully if embedding/grouping fails
            print(f"GROUPING ERROR: {e}")
            import traceback

            traceback.print_exc()
            pass

    # Create question record
    question = Question(
        session_id=session_id,
        group_id=group_id,
        student_hash=student_hash,
        student_name=generate_display_name(),
        text=text,
        embedding=embedding if embedding else None,
        ai_response=ai_response.text if not ai_response.is_flagged else None,
        is_flagged=ai_response.is_flagged,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    status = QuestionStatus.FLAGGED if ai_response.is_flagged else QuestionStatus.POSTED
    return question, status


def get_questions(
    db: Session,
    session_id: uuid.UUID,
    last_seen_timestamp: datetime | None = None,
) -> list[Question]:
    """Get questions for a session, optionally filtered by timestamp."""
    query = select(Question).where(Question.session_id == session_id)

    if last_seen_timestamp:
        query = query.where(Question.created_at > last_seen_timestamp)

    query = query.order_by(Question.created_at)

    return list(db.exec(query).all())
