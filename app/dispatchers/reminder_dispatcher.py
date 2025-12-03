# Handlers for reminder
from commands.create_reminder_cmd import CreateReminderCommand
from commands.cancel_reminder_cmd import CancelReminderCommand
from commands.list_reminders_cmd import ListRemindersCommand
from commands.start_cmd import StartCommand
from commands.help_cmd import HelpCommand

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
    
    async def dispatch(self, message):
        cmd_name = self._get_command_name(message.text)
        command_class = self.commands.get(cmd_name)
        command = command_class(self.repo, self.session, parser=self.parser, reminderScheduler = self.reminderScheduler)
        return await command.execute(message)