# Get all list of reminders
from app.database.models import Reminder
from app.repositories.base import IRepository
from .base import BotCommand
from aiogram import types
from typing import Optional, List, Any

class ListRemindersCommand(BotCommand):
    def __init__(self, repo: IRepository, session: Any):
        self.repo = repo
        self.session = session
        super().__init__()

    async def printAllReminders(self, reminders: List[Reminder], message: types.Message):
        answer_text = ""
        for reminder in reminders:
            answer_text = answer_text + "\n" + (f'''
                #{reminder.id} 📝 {reminder.text}
                ⏰ {reminder.remind_at}
                🔔 {reminder.status} | 🔄 ${reminder.repeated_value}
            ''')
        await message.answer(answer_text)

    async def execute(self, message: types.Message):
        reminders = await self.repo.get_all(self.session)
        await self.printAllReminders(reminders, message)