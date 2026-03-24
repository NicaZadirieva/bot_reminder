from .base import CommandUseCase


class HelpCommand(CommandUseCase):
    """
    Use case для отображения справочной информации.
    Не требует аргументов, просто возвращает текст справки.
    """

    def get_detailed_help(self) -> str:
        return "\n".join(
            ["/help [имя команды]", "Примеры /help:", "/help /remind", "/help"]
        )

    async def execute(self, user_id: int, args=None, **kwargs) -> str:
        """
        Возвращает текст помощи.

        :param user_id: ID пользователя (не используется, но требуется интерфейсом)
        :param args: не используются
        :return: строка с описанием команд
        """
        return "\n".join(
            [
                "/remind <текст> | <время> [| приоритет] [| повтор] Создать новое напоминание",
                "Примеры /remind:",
                "    /remind Купить молоко | 18:00",
                "    /remind Встреча с командой | завтра 15:30",
                "    /remind Позвонить маме | через 2 часа",
                "    /remind Рабочая встреча | 09:00 | HIGH | daily",
                "    /remind Купить подарок | 2024-11-20 19:00 | MEDIUM | once\n",
                "/reminders Показать все ваши напоминания\n",
                "/cancel_reminder <ID> Отменить напоминание по ID\n",
                "/help [имя команды] - Справочная информация по команде\n",
                "/start - Начало работы с ботом",
            ]
        )
