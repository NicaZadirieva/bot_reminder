from app.application.commands.create_reminder_cmd import CreateReminderCommand
from app.application.commands.cancel_reminder_cmd import CancelReminderCommand
from app.application.commands.list_reminders_cmd import ListRemindersCommand
from app.application.commands.start_cmd import StartCommand
from app.application.commands.help_cmd import HelpCommand


class ReminderDispatcher:
    """
    Диспетчер команд для работы с напоминаниями.
    Принимает на вход ID пользователя и текст сообщения,
    определяет команду и делегирует выполнение соответствующему use case.
    """

    def __init__(self, reminder_service, reminder_scheduler, reminder_parser):
        # Создаём экземпляры команд с необходимыми зависимостями
        self._commands = {
            "/remind": CreateReminderCommand(
                reminder_service, reminder_scheduler, reminder_parser
            ),
            "/cancel_reminder": CancelReminderCommand(
                reminder_service, reminder_scheduler
            ),
            "/reminders": ListRemindersCommand(reminder_service),
            "/help": HelpCommand(),
            "/start": StartCommand(),
        }

    async def dispatch(self, user_id: int, text: str) -> str:
        """
        Маршрутизирует сообщение к нужной команде.

        :param user_id: ID пользователя (из Telegram / VK / и т.д.)
        :param text: полный текст сообщения (например, "/remind купить молоко | 18:00")
        :return: текст ответа для отправки пользователю
        """
        if not text or not text.strip():
            return "Пустое сообщение."

        # Разделяем текст на команду и аргументы
        parts = text.strip().split(maxsplit=1)
        command = parts[0]  # например, "/remind"
        args = parts[1] if len(parts) > 1 else ""  # остаток сообщения

        # Проверяем, есть ли команда в зарегистрированных
        if command not in self._commands:
            return f"❌ Неизвестная команда: {command}. Введите /help для справки."

        # Получаем нужный use case и выполняем его
        cmd = self._commands[command]
        return await cmd.execute(user_id=user_id, args=args)
