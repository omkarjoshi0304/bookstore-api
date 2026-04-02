from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bookstore.config import get_settings

settings = get_settings()

connect_args = {}
engine_kwargs: dict = {
    "echo": settings.debug,
}

if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    engine_kwargs.update(
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
    )

engine = create_engine(settings.database_url, connect_args=connect_args, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
