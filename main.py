import asyncio
import logging
import logging.config
import yaml
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
    Настройка логирования на основе log_conf.yaml и параметров из .env.
    """
    # Получаем параметры из настроек
    environment = settings.app.ENVIRONMENT.lower()

    # Создаём директорию для логов, если её нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Загружаем конфигурацию из YAML
    config_path = Path(f"log_conf.{environment}.yaml")  # или укажите полный путь
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 3. Устанавливаем имя файла лога в зависимости от окружения
    config["handlers"]["file"]["filename"] = f"logs/app_{environment}.log"

    # Применяем конфигурацию
    logging.config.dictConfig(config)

    # 4. Отдельная настройка уровней для сторонних библиотек
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
