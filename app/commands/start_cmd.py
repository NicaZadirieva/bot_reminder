from .base import CommandUseCase


class StartCommand(CommandUseCase):
    """
    Use case для приветственного сообщения и краткой справки.
    """

    async def execute(self, user_id: int, args=None, **kwargs) -> str:
        return "\n".join(
            [
                "👋 Привет! Я бот-напоминалка.",
                "",
                "📝 Основные команды:",
                "/remind - Создать напоминание",
                "/reminders - Показать все напоминания",
                "/cancel_reminder - Отменить напоминание",
                "/help - Справка!",
            ]
        )
