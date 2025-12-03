# Handlers for reminder
from app.commands.create_reminder_cmd import CreateReminderCommand
from app.commands.cancel_reminder_cmd import CancelReminderCommand
from app.commands.list_reminders_cmd import ListRemindersCommand
from app.commands.start_cmd import StartCommand
from app.commands.help_cmd import HelpCommand

class ReminderDispatcher:
    def __init__(self, repo, session, parser, reminderScheduler):
        self.commands = {
            '/remind': CreateReminderCommand,
            '/cancel_reminder': CancelReminderCommand,
            '/reminders': ListRemindersCommand,
            '/help': HelpCommand,
            '/start': StartCommand,
        }
        self.session = session
        self.repo = repo
        self.parser = parser
        self.reminderScheduler = reminderScheduler;

    async def remindDispatch(self, message):
        command_class = self.commands.get('/remind')
        command = command_class(self.repo, self.session, parser=self.parser, reminderScheduler = self.reminderScheduler)
        return await command.execute(message)

    async def cancelDispatch(self, message):
        command_class = self.commands.get('/cancel_reminder')
        command = command_class(self.repo, self.session, reminderScheduler = self.reminderScheduler)
        return await command.execute(message)

    async def listDispatch(self, message):
        command_class = self.commands.get('/reminders')
        command = command_class(self.repo, self.session)
        return await command.execute(message)

    async def simpleDispatch(self, message):
        cmd_name = self._get_command_name(message.text)
        command_class = self.commands.get(cmd_name)
        command = command_class()
        return await command.execute(message)

    def _get_command_name(self, message_text: str) -> str:
        if not message_text:
            return ""
        parts = message_text.strip().split()
        if not parts:
            return ""
        command = parts[0]
        if command.startswith('/'):
            return command
        return ""
