# Create remind
from app.services.reminder_service import ReminderService
from .base import BotCommand
from app.parsers import ReminderParser
from aiogram import types
from app.schedulers.reminder_scheduler import ReminderScheduler
import logging
logger = logging.getLogger(__name__)

class CreateReminderCommand(BotCommand):
    def __init__(self, reminderService: ReminderService, reminderScheduler: ReminderScheduler):
        super().__init__()
        self.reminderService = reminderService
        self.reminderScheduler = reminderScheduler

    async def execute(self, message: types.Message):
        # TODO: подумать как заменить \remind, replace
        user_text = message.text.replace("/remind", "")
        try:
            reminder = ReminderParser.parse(user_text, message.from_user.id)
            reminder = await self.reminderService.create_reminder(reminder);
            await self.reminderScheduler.schedule_reminder(reminder)
            await message.answer("✅ Напоминание создано!")
        except Exception as e:
            logger.error(e)
            await message.answer("Формат данных не соответствует команде")

