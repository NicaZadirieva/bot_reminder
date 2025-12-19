# Get all list of reminders
from app.entities.reminder import Reminder, ReminderStatus, RepeatedValue
from app.services.reminder_service import ReminderService
from .base import BotCommand
from aiogram import types
from typing import Optional, List, Any

class ListRemindersCommand(BotCommand):
    def __init__(self, reminderService: ReminderService):
        self.reminderService = reminderService
        super().__init__()

    def ru_repeated_value(self, repeated_value: RepeatedValue):
        repeated_value_str = repeated_value.value
        if repeated_value_str == "daily":
            return "ЕЖЕДНЕВНО"
        elif repeated_value_str == "monthly":
            return "ЕЖЕМЕСЯЧНО"
        elif repeated_value_str == "weekly":
            return "ЕЖЕНЕДЕЛЬНО"
        elif repeated_value_str == "yearly":
            return "ЕЖЕГОДНО"
        elif repeated_value_str == "once":
            return "РАЗОВО"
        else:
            # default
            return "РАЗОВО"

    def ru_status(self, status: ReminderStatus):
        status_str = status.value
        if status_str == "active":
            return "АКТИВНЫЙ"
        elif status_str == "cancelled":
            return "ОТМЕНЕННЫЙ"
        elif status_str == "completed":
            return "ЗАВЕРШЕННЫЙ"
        else:
            # default
            return "АКТИВНЫЙ"

    async def printAllReminders(self, reminders: List[Reminder], message: types.Message):
        answer_text = []
        for reminder in reminders:
            answer_text.append(
                "\n".join([
                f"#{reminder.id} 📝 {reminder.text}",
                f"⏰ {reminder.remind_at}",
                f"🔔 {self.ru_status(reminder.status)} | 🔄 {self.ru_repeated_value(reminder.repeated_value)}"])
            )
        if len(answer_text) > 0:
            await message.answer("\n\n".join(answer_text))
        else:
            await message.answer('Нет напоминаний')

    async def execute(self, message: types.Message):
        reminders = await self.reminderService.get_all_reminders(message.from_user.id)
        await message.answer("📋 Ваши напоминания: \n")
        await self.printAllReminders(reminders, message)