### Thisclass is the base for SQLAlchemy ORM models. Every mapped model should inherit from it.
### SQLAlchemy registers the mapped table information with the base's metadata.
# Alembic uses this metadata to discover the intended database structure.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

