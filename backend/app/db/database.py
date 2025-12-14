from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    """Create all database tables on startup."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
