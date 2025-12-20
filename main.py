import asyncio
import logging.handlers
from aiogram import Router, types
from aiogram.filters import Command
from app.config import config
from app.dispatchers.reminder_dispatcher import ReminderDispatcher
from app.parsers.reminder_parser import ReminderParser
from app.repositories.reminder_repository import ReminderRepository
from app.services.reminder_service import ReminderService
from app.database.connection import async_session
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
    # Читаем конфиг из .env
    environment = config.ENVIRONMENT.lower()
    debug = config.DEBUG
    log_level_str = config.LOG_LEVEL.upper()
    
    # Конвертируем строковый уровень логирования в константу logging
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Формат логирования
    if debug or environment == 'development':
        # Развёрнутый формат для разработки
        log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    else:
        # Компактный формат для продакшена
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Создаём директорию для логов
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    

    # Настраиваем базовую конфигурацию логгера
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # Консольный обработчик
            logging.StreamHandler(),
            # Файловый обработчик
            logging.FileHandler(
                filename=f'logs/app_{environment}.log',
                encoding='utf-8'
            )
        ]
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