import asyncio

from app.commands.fake_message import FakeMessage
from app.commands.help_cmd import HelpCommand
from app.commands.start_cmd import StartCommand
from app.commands.list_reminders_cmd import ListRemindersCommand
from app.database.models import Reminder
from app.repositories.reminder_repository import ReminderRepository
from app.database.connection import async_session
from datetime import datetime, timedelta

from app.repositories.fake_reminder_repository import FakeReminderRepository

async def main():
    helpCmd = HelpCommand()
    await helpCmd.execute(FakeMessage())
    startCmd = StartCommand()
    await startCmd.execute(FakeMessage())
    async with async_session() as session:
        reminder_repo = FakeReminderRepository()
        listAllCmd = ListRemindersCommand(reminder_repo, session)
        await listAllCmd.execute(FakeMessage())

asyncio.run(main())