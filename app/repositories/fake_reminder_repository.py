from app.repositories.fake_repository import IFakeRepository
from app.database.models import Reminder

from datetime import datetime, timedelta

TEST_REMINDERS = [
    # john_doe (telegram_id: 123456789)
    {
        "id": 1,
        "telegram_id": 123456789,
        "text": "Buy milk",
        "remind_at": datetime.now() + timedelta(hours=2),
        "priority": "high",
        "status": "active",
    },
    {
        "id": 2,
        "telegram_id": 123456789,
        "text": "Call mom",
        "remind_at": datetime.now() + timedelta(days=1),
        "priority": "medium",
        "status": "active",
    },
    {
        "id": 3,
        "telegram_id": 123456789,
        "text": "Deadline",
        "remind_at": datetime.now() + timedelta(days=7),
        "priority": "high",
        "status": "active",
    },
    {
        "id": 4,
        "telegram_id": 123456789,
        "text": "Meeting with friend",
        "remind_at": datetime.now() + timedelta(hours=3),
        "priority": "medium",
        "status": "completed",
    },
    {
        "id": 5,
        "telegram_id": 123456789,
        "text": "Buy order",
        "remind_at": datetime.now() - timedelta(hours=1),
        "priority": "high",
        "status": "cancelled",
    },
    
    # jane_smith (telegram_id: 987654321)
    {
        "id": 6,
        "telegram_id": 987654321,
        "text": "Gym",
        "remind_at": datetime.now() + timedelta(hours=1),
        "priority": "medium",
        "status": "active",
    },
    {
        "id": 7,
        "telegram_id": 987654321,
        "text": "Birthday of my friend",
        "remind_at": datetime.now() + timedelta(days=14),
        "priority": "high",
        "status": "active",
    },
    {
        "id": 8,
        "telegram_id": 987654321,
        "text": "Buy gift",
        "remind_at": datetime.now() + timedelta(days=13),
        "priority": "medium",
        "status": "active",
    },
    
    # bob_wilson (telegram_id: 555666777)
    {
        "id": 9,
        "telegram_id": 555666777,
        "text": "Meeting in office",
        "remind_at": datetime.now() + timedelta(hours=4),
        "priority": "high",
        "status": "active",
    },
]


class FakeReminderRepository(IFakeRepository):
    def __init__(self):
        super().__init__(Reminder)
        self.storage = [r.copy() for r in TEST_REMINDERS]
        self.counter = max(r["id"] for r in self.storage) if self.storage else 0

    async def get_by_id(self, session, id: int):
        for reminder in self.storage:
            if (reminder["id"] == id):
                return reminder
        return None
    
    async def get_all(self, session):
        return self.storage.copy()
    
    async def create(self, session, obj: Reminder):
        self.counter += 1
        reminder_data = obj.copy() if isinstance(obj, dict) else {
            "telegram_id": obj.telegram_id,
            "text": obj.text,
            "remind_at": obj.remind_at,
            "priority": obj.priority,
            "status": obj.status
        }
        reminder_data["id"] = self.counter
        self.storage.append(reminder_data)
        return reminder_data
    
    async def update(self, session, id: int, **kwargs):
        for reminder in self.storage:
            if (reminder["id"] == id):
                for key, value in kwargs.items():
                    reminder[key] = value 
                return reminder
        return None

    
    async def delete(self, session, id: int):
        for i, reminder in enumerate(self.storage):
            if reminder["id"] == id:
                deleted = self.storage.pop(i)
                return True
        return False
