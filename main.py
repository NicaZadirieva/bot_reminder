import asyncio
import logging
from pathlib import Path

from aiogram import Bot
from app.config import config
from app.presentation.command_dispatcher import ReminderDispatcher
from app.presentation.telegram_bot_controller import TelegramBotController
from app.infrastructure.repositories import ReminderRepository
from app.services.reminder_service import ReminderService
from app.database import async_session
from app.schedulers.reminder_scheduler import ReminderScheduler

# Если setup_logger остался в этом же файле, оставьте его здесь или импортируйте
# from app.utils.logger import setup_logger


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
        repo = ReminderRepository()
        reminder_service = ReminderService(repo, session)
        bot = Bot(token=config.BOT_TOKEN)  # для reminder_scheduler нужен bot
        reminder_scheduler = ReminderScheduler(reminder_service, bot)
        reminder_dispatcher = ReminderDispatcher(reminder_service, reminder_scheduler)

        controller = TelegramBotController(
            bot_token=config.BOT_TOKEN,
            reminder_dispatcher=reminder_dispatcher,
            reminder_scheduler=reminder_scheduler,
        )

        await controller.start()


if __name__ == "__main__":
    asyncio.run(main())
