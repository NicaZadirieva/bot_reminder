# Get all list of reminders
from app.entities.reminder import Reminder
from app.services.reminder_service import ReminderService
from .base import BotCommand
from aiogram import types
from typing import Optional, List, Any

class ListRemindersCommand(BotCommand):
    def __init__(self, reminderService: ReminderService):
        self.reminderService = reminderService
        super().__init__()

    async def printAllReminders(self, reminders: List[Reminder], message: types.Message):
        answer_text = []
        for reminder in reminders:
            answer_text.append(
                "\n".join([
                f"#{reminder.id} 📝 {reminder.text}",
                f"⏰ {reminder.remind_at}",
                f"🔔 {reminder.status} | 🔄 ${reminder.repeated_value}"])
            )
        if len(answer_text) > 0:
            await message.answer("\n\n".join(answer_text))
        else:
            await message.answer('Нет напоминаний')

    async def execute(self, message: types.Message):
        reminders = await self.reminderService.get_all_reminders(message.from_user.id)
        await message.answer("📋 Ваши напоминания: \n")
        await self.printAllReminders(reminders, message)