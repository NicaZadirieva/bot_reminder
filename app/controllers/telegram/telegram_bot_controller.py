import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

from app.commands import ReminderDispatcher
from app.services import ReminderScheduler

logger = logging.getLogger(__name__)


class TelegramBotController:
    """
    Контроллер для Telegram бота, использующий aiogram.
    Инкапсулирует создание, настройку и запуск бота.
    """

    def __init__(
        self,
        aiogram_bot: Bot,
        reminder_dispatcher: ReminderDispatcher,
        reminder_scheduler: ReminderScheduler,
    ):
        self.bot = aiogram_bot
        self.dp = Dispatcher()
        self.router = Router()
        self.reminder_dispatcher = reminder_dispatcher
        self.reminder_scheduler = reminder_scheduler

        self._setup_handlers()
        self._register_startup_shutdown()

    def _setup_handlers(self) -> None:
        """Регистрирует все обработчики сообщений."""

        @self.router.message(Command("start", "help"))
        async def handle_start_help(message: types.Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_user.id,  # type: ignore
                text=message.text or "",
            )
            await message.answer(response)

        @self.router.message(Command("remind"))
        async def handle_remind(message: types.Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_user.id,  # type: ignore
                text=message.text or "",
            )
            await message.answer(response)

        @self.router.message(Command("cancel_reminder"))
        async def handle_cancel(message: types.Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_user.id,  # type: ignore
                text=message.text or "",
            )
            await message.answer(response)

        @self.router.message(Command("reminders"))
        async def handle_list(message: types.Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_user.id,  # type: ignore
                text=message.text or "",
            )
            await message.answer(response)

        @self.router.message()
        async def handle_unknown(message: types.Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_user.id,  # type: ignore
                text=message.text or "",
            )
            await message.answer(response)

        self.dp.include_router(self.router)

    def _register_startup_shutdown(self) -> None:
        """Регистрирует обработчики запуска и остановки."""

        @self.dp.startup()
        async def on_startup():
            logger.info("Telegram бот запускается...")
            await self.reminder_scheduler.start()

        @self.dp.shutdown()
        async def on_shutdown():
            logger.info("Telegram бот останавливается...")
            await self.reminder_scheduler.shutdown()
            logger.info("Telegram бот остановлен")

    async def start(self) -> None:
        """Запускает поллинг бота."""
        try:
            await self.dp.start_polling(self.bot)
            logger.info("Telegram бот успешно запущен")
        except Exception:
            logger.critical(
                "Ошибка во время запуска Telegram bot. Работа бота невозможна",
                exc_info=True,
            )
        finally:
            await self.bot.session.close()
