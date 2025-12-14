import uuid
import numpy as np
from sqlmodel import Session as DbSession, select

from app.models.question import Question
from app.models.group import QuestionGroup


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if not v1 or not v2:
        return 0.0
    a = np.array(v1)
    b = np.array(v2)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def find_or_create_group(
    db: DbSession,
    session_id: uuid.UUID,
    new_question_text: str,
    new_embedding: list[float],
    threshold: float = 0.85,
) -> uuid.UUID | None:
    """
    Finds a suitable group for the new question based on similarity.
    """
    if not new_embedding:
        return None

    # Fetch all questions from the same session that have an embedding
    # We use db.exec(...).all() which returns a Sequence.
    # SQLModel session.exec returns ScalarResult for select(Model).
    statement = select(Question).where(
        Question.session_id == session_id,
        Question.embedding.is_not(None),  # type: ignore[union-attr]
    )
    results = db.exec(statement).all()

    best_match_q = None
    best_score = -1.0

    for item in results:
        # Check if item is a Row or the Model
        q = item
        # If it's a Row (sqlalchemy < 1.4 or specific config), it might need index access
        # But SQLModel exec usually returns the object.
        # However, checking to be safe if getting unexpected Row objects.
        if hasattr(q, "Question"):
            q = q.Question
        elif not isinstance(q, Question) and hasattr(q, "__getitem__"):
            # It's likely a Row and the model is at index 0
            q = q[0]

        if not isinstance(q, Question):
            # Should not happen if correctly setup
            continue

        if q.embedding is None:
            continue

        score = cosine_similarity(new_embedding, q.embedding)
        if score > threshold and score > best_score:
            best_score = score
            best_match_q = q

    if best_match_q:
        # Match found!
        if best_match_q.group_id:
            # Join existing group
            return best_match_q.group_id
        else:
            # Create a NEW group for both
            # Create group topic from the earlier question (or new one)
            new_group = QuestionGroup(
                session_id=session_id,
                topic=best_match_q.text[:100],  # Simple topic extraction
            )
            db.add(new_group)
            db.commit()
            db.refresh(new_group)

            # Update the matched question to be in this group
            best_match_q.group_id = new_group.id
            db.add(best_match_q)
            db.commit()

            return new_group.id

    return None
