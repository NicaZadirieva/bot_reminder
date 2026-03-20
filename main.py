import asyncio
import logging
import logging.config
import yaml
from pathlib import Path
from aiogram import Bot as AiogramBot
from pytz import timezone
from app.application.domain.entities import PlatformEntity
from app.application.utils.parsers.reminder_parser import ReminderParser
from app.infrastructure.adapters.aiogram_bot import AiogramBotAdapter
from app.core import settings
from app.core.db import async_session
from app.infrastructure.adapters.vk_bot import VkBotAdapter
from app.presentation.command_dispatcher import ReminderDispatcher
from app.presentation.telegram_bot_controller import TelegramBotController
from app.infrastructure.repositories import ReminderRepository
from app.application.services.reminder_service import ReminderService
from app.infrastructure.database import PlatformDb
from app.application.services.reminder_scheduler import ReminderScheduler
from vkbottle import Bot as VkBot

from app.presentation.vk_bot_controller import VkBotController
from app.presentation.vk_client import VKClient


def setup_logger():
    """
    Настройка логирования на основе log_conf.yaml и параметров из .env.
    """
    # Получаем параметры из настроек
    environment = settings.common_app.ENVIRONMENT.lower()

    # Создаём директорию для логов, если её нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Загружаем конфигурацию из YAML
    config_path = Path(f"log_conf.{environment}.yaml")  # или укажите полный путь
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Применяем конфигурацию
    logging.config.dictConfig(config)

    # 4. Отдельная настройка уровней для сторонних библиотек
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


async def main():
    setup_logger()
    async with async_session() as session:
        repo = ReminderRepository(session, PlatformDb.TELEGRAM)
        reminder_service = ReminderService(repo)
        aiogram_bot = AiogramBot(token=settings.tg_app.TG_BOT_TOKEN)
        bot_adapter = AiogramBotAdapter(aiogram_bot)
        reminder_parser = ReminderParser(PlatformEntity.TELEGRAM)
        reminder_scheduler = ReminderScheduler(
            reminder_service, bot_adapter, timezone(settings.common_app.TIMEZONE)
        )
        reminder_dispatcher = ReminderDispatcher(
            reminder_service, reminder_scheduler, reminder_parser
        )

        controller = TelegramBotController(
            aiogram_bot=aiogram_bot,
            reminder_dispatcher=reminder_dispatcher,
            reminder_scheduler=reminder_scheduler,
        )

        await controller.start()


async def main2():
    setup_logger()
    async with async_session() as session:
        repo = ReminderRepository(session, PlatformDb.VK)
        reminder_service = ReminderService(repo)

        vk_client = VKClient(token=settings.vk_app.VK_API_TOKEN)
        bot_adapter = VkBotAdapter(vk_client)  # адаптер использует VKClient

        reminder_parser = ReminderParser(PlatformEntity.VK)
        reminder_scheduler = ReminderScheduler(
            reminder_service, bot_adapter, timezone(settings.common_app.TIMEZONE)
        )
        reminder_dispatcher = ReminderDispatcher(
            reminder_service, reminder_scheduler, reminder_parser
        )

        controller = VkBotController(
            vk_client=vk_client,
            reminder_dispatcher=reminder_dispatcher,
            reminder_scheduler=reminder_scheduler,
        )

        await controller.start()


if __name__ == "__main__":
    asyncio.run(main2())
