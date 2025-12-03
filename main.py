import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from app import config
from app.dispatchers.reminder_dispatcher import ReminderDispatcher
from app.parsers.reminder_parser import ReminderParser
from app.repositories.reminder_repository import ReminderRepository
from app.database.connection import async_session
from aiogram import Dispatcher, Bot

from app.schedulers.reminder_scheduler import ReminderScheduler


async def main():
    async with async_session() as session:
        bot = Bot(token=config.BOT_TOKEN)
        repo = ReminderRepository()
        remindScheduler = ReminderScheduler(session, repo, bot)
        parser = ReminderParser()
        
        reminderDispatcher = ReminderDispatcher(repo, session, parser, remindScheduler)
        router = Router()

        @router.message(Command([
            'remind',
            'cancel_reminder',
            'reminders',
            'start',
            'help'
        ]))
        async def handle_reminder_command(message: types.Message):
            await reminderDispatcher.dispatch(message)

        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

asyncio.run(main())