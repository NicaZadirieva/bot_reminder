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

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    
    reminders = relationship("Reminder", back_populates="user")

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey("users.telegram_id"))
    text = Column(String(200), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    status = Column(Enum(Status), default=Status.ACTIVE)
    created_at = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="reminders")
