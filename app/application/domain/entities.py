from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class PriorityEntity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEntity(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RepeatedValueEntity(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PlatformEntity(Enum):
    VK = "VK"
    TELEGRAM = "TELEGRAM"
    MAX = "MAX"


@dataclass
class ReminderEntity:
    user_id: int
    text: str
    remind_at: datetime
    platform: PlatformEntity
    id: Optional[int] = None
    priority: PriorityEntity = PriorityEntity.MEDIUM
    status: StatusEntity = StatusEntity.ACTIVE
    created_at: Optional[datetime] = None
    repeated_value: RepeatedValueEntity = RepeatedValueEntity.ONCE

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == StatusEntity.ACTIVE

    def mark_completed(self):
        self.status = StatusEntity.COMPLETED
