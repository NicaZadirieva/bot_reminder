from .base import CommandUseCase
from app.application.services.reminder_service import ReminderService
from ..utils.parsers import ReminderParser
from app.application.services.reminder_scheduler import ReminderScheduler
import logging

logger = logging.getLogger(__name__)


class CreateReminderCommand(CommandUseCase):
    """
    Use case для создания напоминания.
    Ожидает аргументы в свободной форме, которые парсятся через ReminderParser.
    """

    def __init__(
        self, reminder_service: ReminderService, reminder_scheduler: ReminderScheduler
    ):
        self.reminder_service = reminder_service
        self.reminder_scheduler = reminder_scheduler

    async def execute(self, user_id: int, args=None, **kwargs) -> str:
        """
        Выполняет создание напоминания.

        :param user_id: ID пользователя, создающего напоминание
        :param args: строка с параметрами напоминания (например, "Завтра в 10:0 позвонить маме")
        :return: текст ответа для пользователя
        """
        # Проверяем, что аргументы переданы
        if not args or not args.strip():
            return "❌ Укажите параметры напоминания. Пример: /remind Завтра в 10:0 позвонить маме"

        # Парсим текст в объект напоминания
        try:
            reminder = ReminderParser.parse(args, user_id)
        except Exception as e:
            logger.error(f"Ошибка парсинга напоминания: {e}")
            return "❌ Формат данных не соответствует команде. Проверьте правильность ввода."

        # Сохраняем напоминание в базе данных
        try:
            reminder = await self.reminder_service.create_reminder(reminder)
        except Exception as e:
            logger.error(f"Ошибка создания напоминания в БД: {e}")
            return "❌ Не удалось создать напоминание. Попробуйте позже."

        # Планируем задачу в шедулере
        try:
            await self.reminder_scheduler.schedule_reminder(reminder)
        except Exception as e:
            logger.error(f"Ошибка планирования напоминания: {e}")
            # Напоминание создано в БД, но не запланировано – уведомляем пользователя
            return "⚠️ Напоминание сохранено, но не удалось запланировать. Обратитесь в поддержку."

        return "✅ Напоминание создано!"
