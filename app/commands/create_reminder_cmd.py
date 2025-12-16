# Create remind
from .base import BotCommand
from app.parsers.reminder_parser import ReminderParser
from app.repositories.base import IRepository
from aiogram import types
from typing import Optional, List, Any
from app.schedulers.reminder_scheduler import ReminderScheduler
import logging
logger = logging.getLogger(__name__)

class CreateReminderCommand(BotCommand):
    def __init__(self, repo: IRepository, session: Any, parser: ReminderParser, reminderScheduler: ReminderScheduler):
        super().__init__()
        self.parser = parser
        self.repo = repo
        self.session = session
        self.reminderScheduler = reminderScheduler

    async def execute(self, message: types.Message):
        # TODO: подумать как заменить \remind, replace
        user_text = message.text.replace("/remind", "")
        try:
            reminder = self.parser.parse(user_text, message.from_user.id)
            await self.repo.create(self.session, reminder);
            await self.reminderScheduler.schedule_reminder(reminder)
            await message.answer("✅ Напоминание создано!")
        except Exception as e:
            logger.error(e)
            await message.answer("Формат данных не соответствует команде")

