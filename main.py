import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from app.config import config
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

        @router.message(Command(
            'start',
            'help'
        ))
        async def handle_reminder_simple_command(message: types.Message):
            await reminderDispatcher.simpleDispatch(message)

        @router.message(Command(
            'remind'
        ))
        async def handle_reminder_create_command(message: types.Message):
            await reminderDispatcher.remindDispatch(message)

        @router.message(Command(
            'cancel_reminder'
        ))
        async def handle_reminder_cancel_command(message: types.Message):
            await reminderDispatcher.cancelDispatch(message)

        
        @router.message(Command(
            'reminders'
        ))
        async def handle_reminder_list_command(message: types.Message):
            await reminderDispatcher.listDispatch(message)

        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

asyncio.run(main())