from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Priority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RepeatedValue(PyEnum):
    ONCE = "ONCE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    remind_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.MEDIUM)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    repeated_value: Mapped[RepeatedValue] = mapped_column(
        Enum(RepeatedValue, name="repeated_value_enum"),
        nullable=False,
        default=RepeatedValue.ONCE,
    )
