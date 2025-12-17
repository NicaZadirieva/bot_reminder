import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from app.config import config
from app.dispatchers.reminder_dispatcher import ReminderDispatcher
from app.parsers.reminder_parser import ReminderParser
from app.repositories.reminder_repository import ReminderRepository
from app.services.reminder_service import ReminderService
from app.database.connection import async_session
from aiogram import Dispatcher, Bot

from app.schedulers.reminder_scheduler import ReminderScheduler

import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    )
    
    # Отключить шум от сторонних библиотек (поставить им уровень выше)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


async def main():
    setup_logger()
    async with async_session() as session:
        bot = Bot(token=config.BOT_TOKEN)
        repo = ReminderRepository()
        reminderService = ReminderService(repo, session)
        remindScheduler = ReminderScheduler(reminderService, bot)
        parser = ReminderParser()
        
        reminderDispatcher = ReminderDispatcher(reminderService, parser, remindScheduler)
        router = Router()

        @router.message(Command(
            'start',
            'help'
        ))
        async def handle_reminder_help_command(message: types.Message):
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

        @router.message()  # ← Без фильтров - ловит ВСЕ остальные сообщения
        async def handle_no_match(message: types.Message):
            """Обработать сообщения, которые не совпадают ни с чем"""
            await message.answer(
                "❌ Команда не найдена.\n\n"
                "Используй /help для списка команд"
            )

        dp = Dispatcher()
        dp.include_router(router)
        

        # Регистрируем обработчики
        async def on_startup():
            """Вызовется при старте бота"""
            await remindScheduler.start()

        async def on_shutdown():
            """Вызовется при остановке бота"""
            await remindScheduler.shutdown()

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await dp.start_polling(bot)


asyncio.run(main())