from app.repositories.fake_repository import IFakeRepository
from app.database.models import User

TEST_USERS_DATA = [
    {"id": 0, "telegram_id": 123456789, "username": "john_doe"},
    {"id": 1, "telegram_id": 987654321, "username": "jane_smith"},
    {"id": 2, "telegram_id": 555666777, "username": "bob_wilson"},
    {"id": 3, "telegram_id": 111222333, "username": "alice_brown"},
    {"id": 4, "telegram_id": 444555666, "username": "charlie_davis"},
]

class FakeUserRepository(IFakeRepository):
    def __init__(self):
        super().__init__(User)
        self.storage = [u.copy() for u in TEST_USERS_DATA]
        self.counter = max(u["id"] for u in self.storage) if self.storage else 0

    async def get_by_id(self, session, id: int):
        for user in self.storage:
            if (user["id"] == id):
                return user
        return None
    
    async def get_all(self, session):
        return self.storage.copy()
    
    async def create(self, session, obj: User):
        self.counter += 1
        user_data = obj.copy() if isinstance(obj, dict) else {
            "telegram_id": obj.telegram_id,
            "username": obj.username,
        }
        user_data["id"] = self.counter
        self.storage.append(user_data)
        return user_data
    
    async def update(self, session, id: int, **kwargs):
        for user in self.storage:
            if (user["id"] == id):
                for key, value in kwargs.items():
                    user[key] = value 
                return user
        return None

    
    async def delete(self, session, id: int):
        for i, user in enumerate(self.storage):
            if user["id"] == id:
                deleted = self.storage.pop(i)
                return True
        return False
