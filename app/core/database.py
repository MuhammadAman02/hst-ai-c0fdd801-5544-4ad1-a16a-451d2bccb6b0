```python
"""Database configuration and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from contextlib import contextmanager
from typing import Generator
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create engine with proper configuration
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """Drop all database tables"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup"""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI"""
    with get_db_session() as session:
        yield session
```