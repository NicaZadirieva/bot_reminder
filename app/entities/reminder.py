from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ReminderStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RepeatedValue(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class Reminder:
    telegram_id: int
    text: str
    remind_at: datetime
    
    id: Optional[int] = None
    priority: Priority = Priority.MEDIUM
    status: ReminderStatus = ReminderStatus.ACTIVE
    created_at: Optional[datetime] = None
    repeated_value: RepeatedValue = RepeatedValue.ONCE
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def is_active(self) -> bool:
        return self.status == ReminderStatus.ACTIVE
    
    def mark_completed(self):
        self.status = ReminderStatus.COMPLETED
