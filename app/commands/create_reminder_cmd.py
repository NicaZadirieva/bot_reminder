from .base import CommandUseCase
from app.services import ReminderService, ReminderScheduler
from app.utils.parsers import ReminderParser
import logging

logger = logging.getLogger(__name__)


class CreateReminderCommand(CommandUseCase):
    """
    Use case для создания напоминания.
    Ожидает аргументы в свободной форме, которые парсятся через ReminderParser.
    """

    def __init__(
        self,
        reminder_service: ReminderService,
        reminder_scheduler: ReminderScheduler,
        reminder_parser: ReminderParser,
    ):
        self.reminder_service = reminder_service
        self.reminder_scheduler = reminder_scheduler
        self.reminder_parser = reminder_parser

    def get_detailed_help(self) -> str:
        return "\n".join(
            [
                "/remind <текст> | <время> [| приоритет] [| повтор] - создать новое напоминание",
                "\n",
                "Поддерживаемые форматы времени:",
                "HH:MM — Сегодня в указанное время (если прошло → на завтра)",
                "завтра HH:MM — Завтра в указанное время",
                "через X часов — Через X часов",
                "через X минут — Через X минут",
                "YYYY-MM-DD HH:MM — Конкретная дата и время\n",
                "Приоритеты: (для маркировки напоминания. необязательно)",
                "LOW или низкий — Низкий приоритет",
                "MEDIUM или средний — Средний приоритет (по умолчанию)",
                "HIGH или высокий — Высокий приоритет",
                "\n",
                "Повторения (необязательно):",
                "ONCE или разово — Один раз (по умолчанию)",
                "DAILY или ежедневно — Каждый день в указанное время",
                "WEEKLY или еженедельно — Каждую неделю",
                "MONTHLY или ежемесячно — Каждый месяц",
                "YEARLY или ежегодно - Каждый год",
            ]
        )

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
            reminder = self.reminder_parser.parse(args, user_id)
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
