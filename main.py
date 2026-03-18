import asyncio
import logging
from pathlib import Path
from aiogram import Bot as AiogramBot
from pytz import timezone
from app.infrastructure.adapters.aiogram_bot import AiogramBotAdapter
from app.core import settings
from app.presentation.command_dispatcher import ReminderDispatcher
from app.presentation.telegram_bot_controller import TelegramBotController
from app.infrastructure.repositories import ReminderRepository
from app.application.services.reminder_service import ReminderService
from app.infrastructure.database import async_session
from app.application.services.reminder_scheduler import ReminderScheduler


def setup_logger():
    """
    Настройка и возврат логгера на основе конфигурации из .env

    Переменные .env:
    - ENVIRONMENT: development, staging, production
    - DEBUG: True/False
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL, EXCEPTION
    """
    environment = settings.app.ENVIRONMENT.lower()
    debug = settings.app.DEBUG
    log_level_str = settings.app.LOG_LEVEL.upper()

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
        repo = ReminderRepository()
        reminder_service = ReminderService(repo, session)
        aiogram_bot = AiogramBot(token=settings.app.BOT_TOKEN)
        bot_adapter = AiogramBotAdapter(aiogram_bot)

        reminder_scheduler = ReminderScheduler(
            reminder_service, bot_adapter, timezone(settings.app.TIMEZONE)
        )
        reminder_dispatcher = ReminderDispatcher(reminder_service, reminder_scheduler)

        controller = TelegramBotController(
            aiogram_bot=aiogram_bot,
            reminder_dispatcher=reminder_dispatcher,
            reminder_scheduler=reminder_scheduler,
        )

        await controller.start()


if __name__ == "__main__":
    asyncio.run(main())
