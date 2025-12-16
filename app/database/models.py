from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from enum import Enum as PyEnum

class Base(DeclarativeBase):
    pass

class Priority(PyEnum):  # ← Наследуй от PyEnum
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(PyEnum):  # ← Наследуй от PyEnum
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RepeatedValue(PyEnum):  # ← Наследуй от PyEnum
    ONCE = "ONCE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    text = Column(String(200), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    priority = Column(
        SQLEnum(Priority),  # ← SQLEnum используется только здесь в Column
        default=Priority.MEDIUM
    )
    status = Column(
        SQLEnum(Status),  # ← SQLEnum используется только здесь в Column
        default=Status.ACTIVE
    )
    created_at = Column(DateTime, default=datetime.now)
    repeated_value = Column(
        SQLEnum(RepeatedValue, name="repeated_value_enum"),
        nullable=False,
        default=RepeatedValue.ONCE
    )
