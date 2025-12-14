import os

from google import genai

from app.core.config import get_settings


def generate_embedding(text: str) -> list[float]:
    """Generate a vector embedding for the given text using Google Gen AI."""
    settings = get_settings()
    # The client will automatically pick up GOOGLE_API_KEY from env if set,
    # but we set it explicitly to be safe as done in ai_agent_service.
    os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

    client = genai.Client(api_key=settings.google_api_key)

    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )

    # Check the structure of response. It usually has 'embedding' or 'embeddings'.
    # For a single string input, it should return one embedding.
    if response.embeddings:
        return response.embeddings[0].values

    # Fallback/Error handling (simplified)
    return []
