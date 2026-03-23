from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .priority import Priority
from .status import Status
from .repeated_value import RepeatedValue
from .platform import Platform


@dataclass
class Reminder:
    user_id: int
    text: str
    remind_at: datetime
    platform: Platform
    id: Optional[int] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.ACTIVE
    created_at: Optional[datetime] = None
    repeated_value: RepeatedValue = RepeatedValue.ONCE

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == Status.ACTIVE

    def mark_completed(self):
        self.status = Status.COMPLETED
