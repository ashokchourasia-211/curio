from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import v1_router
from app.db.database import create_db_and_tables

# Import models to register them with SQLModel metadata
from app.models import Session, Question, QuestionGroup  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan - create tables on startup."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Curio API",
    description="Anonymous Classroom Q&A with AI-Augmented Answers",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(v1_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "app": "Curio API"}
