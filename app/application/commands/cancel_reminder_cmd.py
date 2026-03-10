from .base import CommandUseCase
from app.services.reminder_service import ReminderService
from app.schedulers.reminder_scheduler import ReminderScheduler


class CancelReminderCommand(CommandUseCase):
    """
    Use case для отмены напоминания по его ID.
    Ожидает аргумент — число (ID напоминания).
    """

    def __init__(
        self, reminder_service: ReminderService, reminder_scheduler: ReminderScheduler
    ):
        self.reminder_service = reminder_service
        self.reminder_scheduler = reminder_scheduler

    async def execute(self, user_id: int, args=None, **kwargs) -> str:
        """
        Выполняет отмену напоминания.

        :param user_id: ID пользователя, который хочет отменить напоминание
        :param args: строка с ID напоминания (например, "123")
        :param kwargs: не используются, но могут быть переданы из диспетчера
        :return: текст ответа для пользователя
        """
        # Проверяем, что аргумент передан
        if not args or not args.strip():
            return "❌ Укажите ID напоминания. Пример: /cancel_reminder 123"

        # Парсим ID (берём первое слово из аргументов)
        try:
            reminder_id = int(args.strip().split()[0])
        except ValueError:
            return "❌ ID должен быть числом"

        # Пытаемся отменить напоминание в базе данных
        updated = await self.reminder_service.cancel_reminder_by_id(
            reminder_id, user_id
        )

        if not updated:
            return f"❌ Напоминание #{reminder_id} не найдено или уже отменено"

        # Если в базе отменили успешно, пробуем удалить задачу из планировщика
        try:
            await self.reminder_scheduler.cancel_reminder_job(reminder_id, user_id)
        except Exception as e:
            # TODO: Логируем ошибку (можно добавить logger в конструктор)
            # Здесь просто возвращаем предупреждение, но считаем операцию выполненной
            return f"✅ Напоминание #{reminder_id} отменено, но возникла проблема при удалении из планировщика. Обратитесь в поддержку, если напоминание продолжит приходить."

        return f"✅ Напоминание #{reminder_id} отменено"
