import asyncio
from aiogram import Bot as AiogramBot
from pytz import timezone
from app.entities.entities import PlatformEntity
from app.utils.LoggerUtils import LoggerUtils
from app.utils.parsers.reminder_parser import ReminderParser
from app.adapters.aiogram_bot import AiogramBotAdapter
from app.core import settings
from app.core.db import async_session
from app.adapters.vk_bot import VkBotAdapter
from app.commands.dispatchers.remind_dispatcher import ReminderDispatcher
from app.controllers.telegram.telegram_bot_controller import TelegramBotController
from app.repositories.reminder_repository import ReminderRepository
from app.services.reminder_service import ReminderService
from app.models.models import Platform as PlatformDb
from app.services.reminder_scheduler import ReminderScheduler

from app.controllers.vk.vk_bot_controller import VkBotController
from app.controllers.vk.vk_client import VKClient


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
