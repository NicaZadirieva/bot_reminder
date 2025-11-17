import asyncio

from app.commands.fake_message import FakeMessage
from app.commands.help_cmd import HelpCommand
from app.commands.start_cmd import StartCommand
from app.database.models import Reminder
from app.repositories.reminder_repository import ReminderRepository
from app.database.connection import async_session
from datetime import datetime, timedelta

reminder_repo = ReminderRepository()


async def main():
    helpCmd = HelpCommand()
    await helpCmd.execute(FakeMessage())
    startCmd = StartCommand()
    await startCmd.execute(FakeMessage())

asyncio.run(main())