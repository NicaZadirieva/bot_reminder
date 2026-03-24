from typing import Optional
from app.commands.base import CommandUseCase
from app.commands.create_reminder_cmd import CreateReminderCommand
from app.commands.cancel_reminder_cmd import CancelReminderCommand
from app.commands.list_reminders_cmd import ListRemindersCommand
from app.commands.start_cmd import StartCommand
from app.commands.help_cmd import HelpCommand
from .base import BaseCommandDispatcher


class CommandDispatcher(BaseCommandDispatcher):
    """
    Диспетчер команд для работы с напоминаниями.
    Принимает на вход ID пользователя и текст сообщения,
    определяет команду и делегирует выполнение соответствующему use case.
    """

    def __init__(self, reminder_service, reminder_scheduler, reminder_parser):
        # Создаём экземпляры команд с необходимыми зависимостями
        self._helpCommand = HelpCommand()
        self._commands = {
            "/remind": CreateReminderCommand(
                reminder_service, reminder_scheduler, reminder_parser
            ),
            "/cancel_reminder": CancelReminderCommand(
                reminder_service, reminder_scheduler
            ),
            "/reminders": ListRemindersCommand(reminder_service),
            "/help": self._helpCommand,
            "/start": StartCommand(),
        }

    def __get_detailed_info__(self, args: list[str]) -> Optional[str]:
        if len(args) > 0:
            if len(args) != 1:
                return "❌ Требуется только один аргумент"

            command = self._commands.get(args[0].strip())
            if isinstance(command, CommandUseCase):
                return command.get_detailed_help()
            else:
                return f"❌ Неизвестная команда: {args[0]}. Введите /help для справки."
        return None

    async def dispatch(self, user_id: int, text: str) -> str:
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

        if cmd is self._helpCommand:
            help_info = await self._helpCommand.execute(user_id=user_id, args=args)
            return self.__get_detailed_info__(args=args.split()) or help_info

        return await cmd.execute(user_id=user_id, args=args)
