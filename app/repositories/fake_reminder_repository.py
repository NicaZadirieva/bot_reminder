from app.repositories.fake_repository import IFakeRepository
from typing import Optional, List, Any
from app.database.models import Reminder

from datetime import datetime, timedelta

TEST_REMINDERS: List[Reminder] = [
    Reminder(
        id =  1,
        telegram_id =  123456789,
        text = "Buy milk",
        remind_at = datetime.now() + timedelta(hours=2),
        priority =  "high",
        status =  "active",
        repeated_value = "once"
    ),
    Reminder(
        id =  2,
        telegram_id =  123456789,
        text = "Call mom",
        remind_at = datetime.now() + timedelta(days=1),
        priority =  "medium",
        status =  "active",
        repeated_value = "once"
    ),
    Reminder(
        id =  3,
        telegram_id =  123456789,
        text = "Deadline",
        remind_at = datetime.now() + timedelta(days=7),
        priority =  "high",
        status =  "active",
        repeated_value = "once"
    ),
    Reminder(
        id = 4,
        telegram_id =  123456789,
        text = "Meeting with friend",
        remind_at = datetime.now() + timedelta(hours=3),
        priority =  "medium",
        status =  "completed",
        repeated_value = "once"
    ),
    Reminder(
        id = 5,
        telegram_id =  123456789,
        text = "Buy order",
        remind_at = datetime.now() - timedelta(hours=1),
        priority =  "high",
        status =  "cancelled",
        repeated_value = "once"
    ),
    
    # jane_smith (telegram_id: 987654321)
    Reminder(
        id = 6,
        telegram_id =  987654321,
        text = "Gym",
        remind_at = datetime.now() + timedelta(hours=1),
        priority =  "medium",
        status =  "active",
        repeated_value = "once"
    ),
    Reminder(
        id = 7,
        telegram_id =  987654321,
        text = "Birthday of my friend",
        remind_at = datetime.now() + timedelta(days=14),
        priority =  "high",
        status =  "active",
        repeated_value = "once"
    ),
    Reminder(
        id = 8,
        telegram_id =  987654321,
        text = "Buy gift",
        remind_at = datetime.now() + timedelta(days=13),
        priority =  "medium",
        status =  "active",
        repeated_value = "once"
    ),   
    # bob_wilson (telegram_id: 555666777)
    Reminder(
        id = 9,
        telegram_id = 555666777,
        text = "Meeting in office",
        remind_at = datetime.now() + timedelta(hours=4),
        priority =  "high",
        status =  "active",
        repeated_value = "once"
    )
]


class FakeReminderRepository(IFakeRepository):
    def __init__(self):
        super().__init__(Reminder)
        self.storage: List[Reminder] = [r for r in TEST_REMINDERS]
        self.counter = max(r.id for r in self.storage) if self.storage else 0

    async def get_by_id(self, session: Any, id: int) -> Optional[Reminder]:
        for reminder in self.storage:
            if reminder.id == id:
                return reminder
        return None
    
    async def get_all(self, session: Any) -> List[Reminder]:
        return self.storage.copy()
    
    
    async def create(self, session: Any, obj: Reminder) -> Reminder:
        self.counter += 1
        
        if isinstance(obj, Reminder):
            reminder = Reminder(
                id=self.counter,
                telegram_id=obj.telegram_id,
                text=obj.text,
                remind_at=obj.remind_at,
                priority=obj.priority,
                status=obj.status,
                repeated_value=obj.repeated_value
            )
        else:
            reminder = Reminder(
                id=self.counter,
                telegram_id=obj.get("telegram_id"),
                text=obj.get("text"),
                remind_at=obj.get("remind_at"),
                priority=obj.get("priority"),
                status=obj.get("status"),
                repeated_value=obj.get("repeated_value")
            )
        
        self.storage.append(reminder)
        return reminder
    
    async def update(self, session: Any, id: int, **kwargs) -> Optional[Reminder]:
        for reminder in self.storage:
            if reminder.id == id:
                for key, value in kwargs.items():
                    setattr(reminder, key, value)
                return reminder
        return None

    async def delete(self, session: Any, id: int) -> bool:
        for i, reminder in enumerate(self.storage):
            if reminder.id == id:
                self.storage.pop(i)
                return True
        return False