import asyncio
import logging.handlers
from aiogram import Router, types
from aiogram.filters import Command
from app.config import config
from app.presentation.command_dispatcher import ReminderDispatcher
from app.repositories import ReminderRepository
from app.services.reminder_service import ReminderService
from app.database import async_session
from aiogram import Dispatcher, Bot
from pathlib import Path

from app.schedulers.reminder_scheduler import ReminderScheduler

import logging


def setup_logger():
    """
    Настройка и возврат логгера на основе конфигурации из .env

    Переменные .env:
    - ENVIRONMENT: development, staging, production
    - DEBUG: True/False
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL, EXCEPTION
    """
    environment = config.ENVIRONMENT.lower()
    debug = config.DEBUG
    log_level_str = config.LOG_LEVEL.upper()

    log_level = getattr(logging, log_level_str, logging.INFO)

    if debug or environment == "development":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    else:
        log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                filename=f"logs/app_{environment}.log", encoding="utf-8"
            ),
        ],
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


async def main():
    setup_logger()
    async with async_session() as session:
        bot = Bot(token=config.BOT_TOKEN)
        repo = ReminderRepository()
        reminder_service = ReminderService(repo, session)
        remind_scheduler = ReminderScheduler(reminder_service, bot)

        # Создаём диспетчер команд с необходимыми зависимостями
        reminder_dispatcher = ReminderDispatcher(reminder_service, remind_scheduler)
        router = Router()

        # Обработчик команд /start и /help
        @router.message(Command("start", "help"))
        async def handle_start_help(message: types.Message):
            response = await reminder_dispatcher.dispatch(
                user_id=message.from_user.id, text=message.text or ""
            )
            await message.answer(response)

        # Обработчик команды /remind
        @router.message(Command("remind"))
        async def handle_remind(message: types.Message):
            response = await reminder_dispatcher.dispatch(
                user_id=message.from_user.id, text=message.text or ""
            )
            await message.answer(response)

        # Обработчик команды /cancel_reminder
        @router.message(Command("cancel_reminder"))
        async def handle_cancel(message: types.Message):
            response = await reminder_dispatcher.dispatch(
                user_id=message.from_user.id, text=message.text or ""
            )
            await message.answer(response)

        # Обработчик команды /reminders
        @router.message(Command("reminders"))
        async def handle_list(message: types.Message):
            response = await reminder_dispatcher.dispatch(
                user_id=message.from_user.id, text=message.text or ""
            )
            await message.answer(response)

        # Обработчик всех остальных сообщений (неизвестные команды или просто текст)
        @router.message()
        async def handle_unknown(message: types.Message):
            response = await reminder_dispatcher.dispatch(
                user_id=message.from_user.id, text=message.text or ""
            )
            # Если диспетчер вернул сообщение об неизвестной команде — отлично, иначе просто отвечаем
            await message.answer(response)

        dp = Dispatcher()
        dp.include_router(router)

        async def on_startup():
            await remind_scheduler.start()

        async def on_shutdown():
            await remind_scheduler.shutdown()

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
