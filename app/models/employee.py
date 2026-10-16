from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    employee_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    department: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="ACTIVE",
    )

