from typing import List

from app.models import Reminder
from app.services import ReminderService
from app.utils.translators.StatusTranslator import StatusTranslator
from app.utils.translators.FreqTranslator import FreqTranslator
from .base import CommandUseCase


class ListRemindersCommand(CommandUseCase):
    """
    Use case для отображения списка всех напоминаний пользователя.
    Не требует аргументов.
    """

    def __init__(self, reminder_service: ReminderService):
        self.reminder_service = reminder_service

    async def _format_reminders(self, reminders: List[Reminder]) -> str:
        """
        Формирует текст из списка напоминаний.
        Если список пуст, возвращает сообщение об этом.
        """
        if not reminders:
            return "Нет напоминаний"

        formatted_items = []
        for reminder in reminders:
            formatted_items.append(
                "\n".join(
                    [
                        f"#{reminder.id} 📝 {reminder.text}",
                        f"⏰ {reminder.remind_at}",
                        f"🔔 {StatusTranslator.from_eng_to_ru(reminder.status)} | 🔄 {FreqTranslator.eng_to_ru(reminder.repeated_value)}",
                    ]
                )
            )

        # Объединяем элементы с пустой строкой между ними
        return "📋 Ваши напоминания:\n\n" + "\n\n".join(formatted_items)

    async def execute(self, user_id: int, args=None, **kwargs) -> str:
        """
        Возвращает отформатированный список напоминаний пользователя.
        """
        reminders = await self.reminder_service.get_all_reminders(user_id)
        return await self._format_reminders(reminders)
