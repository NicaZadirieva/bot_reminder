import asyncio
from pathlib import Path
from aiogram import Bot as AiogramBot
from pytz import timezone
from app.application.domain.entities import PlatformEntity
from app.application.utils.LoggerUtils import LoggerUtils
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

from app.presentation.vk_bot_controller import VkBotController
from app.presentation.vk_client import VKClient


async def run_tg_bot():
    async with async_session() as session:
        repo = ReminderRepository(session, PlatformDb.TELEGRAM)
        reminder_service = ReminderService(repo)
        aiogram_bot = AiogramBot(token=settings.tg_app.TG_BOT_TOKEN)  # type: ignore
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


async def run_vk_bot():
    async with async_session() as session:
        repo = ReminderRepository(session, PlatformDb.VK)
        reminder_service = ReminderService(repo)

        vk_client = VKClient(token=settings.vk_app.VK_API_TOKEN)  # type: ignore
        bot_adapter = VkBotAdapter(vk_client)

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
    LoggerUtils.setup_logger()

    if settings.vk_app.VK_RUN:
        asyncio.run(run_vk_bot())
    if settings.tg_app.TG_RUN:
        asyncio.run(run_tg_bot())
