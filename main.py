import asyncio
from aiogram import Bot as AiogramBot

from app.entities import PlatformEntity
from app.utils.LoggerUtils import LoggerUtils
from app.utils.parsers import ReminderParser
from app.adapters import AiogramBotAdapter, VkBotAdapter
from app.core import settings, async_session
from app.commands import ReminderDispatcher
from app.controllers import TelegramBotController, VkBotController, VKClient
from app.repositories import ReminderRepository
from app.services import ReminderService, ReminderScheduler
from app.models import PlatformDb


async def run_tg_bot():
    async with async_session() as session:
        repo = ReminderRepository(session, PlatformDb.TELEGRAM)
        reminder_service = ReminderService(repo)
        aiogram_bot = AiogramBot(token=settings.tg_app.TG_BOT_TOKEN)  # type: ignore
        bot_adapter = AiogramBotAdapter(aiogram_bot)
        reminder_parser = ReminderParser(PlatformEntity.TELEGRAM)
        reminder_scheduler = ReminderScheduler(reminder_service, bot_adapter)
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
        reminder_scheduler = ReminderScheduler(reminder_service, bot_adapter)
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
