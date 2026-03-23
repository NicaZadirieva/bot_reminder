from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .priority import Priority
from .repeated_value import RepeatedValue
from .status import Status
from .platform import Platform


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
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
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
