from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .priority_entity import PriorityEntity
from .status_entity import StatusEntity
from .repeated_value_entity import RepeatedValueEntity
from .platform_entity import PlatformEntity


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
