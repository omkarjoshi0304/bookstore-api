from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bookstore.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,         # Verify connections before use
    pool_size=10,               # Max persistent connections
    max_overflow=20,            # Extra connections under load
    pool_recycle=3600,          # Recycle connections after 1 hour
    echo=settings.debug,        # SQL logging in debug mode
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
