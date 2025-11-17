from aiogram import types
from datetime import datetime

class FakeMessage(types.Message):
    def __init__(self):
        chat = types.Chat(
            id=123456789,
            type="private"
        )
        
        user = types.User(
            id=123456789,
            is_bot=False,
            first_name="Test",
            last_name="User"
        )
        
        super().__init__(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            from_user=user
        )
    

    async def answer(self, text: str):
        print(text)