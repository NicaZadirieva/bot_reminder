from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class Priority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RepeatedValue(PyEnum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    text = Column(String(200), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    status = Column(Enum(Status), default=Status.ACTIVE)
    created_at = Column(DateTime, default=datetime.now)
    repeated_value = Column(Enum(RepeatedValue, name='repeated_value_enum'), default=RepeatedValue.ONCE, nullable=True)
