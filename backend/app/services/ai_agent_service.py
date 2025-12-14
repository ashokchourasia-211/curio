import asyncio
from dataclasses import dataclass

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


SYSTEM_PROMPT = """You are Curio AI, an educational assistant for anonymous classroom Q&A.

## Your Role
You help students understand concepts by providing clear, educational answers.

## Safety Rules (CRITICAL - Check FIRST)
Before answering, check if the question contains:
- Hate speech, bullying, or harassment
- Profanity or inappropriate language
- Off-topic or spam content
- Requests for harmful information

If ANY of these are detected, respond ONLY with: "FLAGGED: [reason]"

## Response Guidelines
If the question is safe:
1. Provide a clear, concise explanation
2. Use simple language appropriate for students
3. Include examples when helpful
4. Keep responses under 200 words
5. Be encouraging and supportive

Remember: You're helping students learn without judgment!
"""


@dataclass
class AIResponse:
    """Response from the AI agent."""

    text: str
    is_flagged: bool


async def process_question(question_text: str) -> AIResponse:
    """Process a student question through the AI agent.

    Returns the AI response and whether the content was flagged.
    """
    # Ensure API key is set for Google ADK
    import os

    from app.core.config import get_settings

    settings = get_settings()
    os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)

    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="curio_tutor",
        instruction=SYSTEM_PROMPT,
    )

    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="curio",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="curio",
        user_id="anonymous",
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=question_text)],
    )

    response_text = ""
    async for event in runner.run_async(
        session_id=session.id,
        user_id="anonymous",
        new_message=content,
    ):
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text

    # Check if the response indicates flagged content
    is_flagged = response_text.strip().upper().startswith("FLAGGED:")

    if is_flagged:
        return AIResponse(text="Message flagged for review.", is_flagged=True)

    return AIResponse(text=response_text.strip(), is_flagged=False)


def process_question_sync(question_text: str) -> AIResponse:
    """Synchronous wrapper for process_question."""
    return asyncio.run(process_question(question_text))
