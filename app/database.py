###  app/database.py with the following complete version if you have not already done so
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:     # Provides the session
        yield db  # In Python, yield makes a function a generator. In a FastAPI dependency, it also allows FastAPI to separate setup from cleanup.

    finally:
        db.close()




'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(  
    bind=engine,
    autoflush=False,  # Disables automatic flushing before ORM queries
    expire_on_commit=False, # Keeps loaded object attributes available after commit, subject to normal ORM limitations
)

# SessionLocal -- A factory for creating database sessions
'''