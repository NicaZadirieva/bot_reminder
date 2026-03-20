import asyncio
import logging
from vkbottle import Bot
from vkbottle.bot import BotLabeler, Message
from app.presentation.command_dispatcher import ReminderDispatcher
from app.application.services.reminder_scheduler import ReminderScheduler

logger = logging.getLogger(__name__)


class VkBotController:
    """
    Контроллер для VK бота, использующий vkbottle.
    Инкапсулирует создание, настройку и запуск бота.
    """

    def __init__(
        self,
        vk_bot: Bot,
        reminder_dispatcher: ReminderDispatcher,
        reminder_scheduler: ReminderScheduler,
    ):
        self.bot = vk_bot
        self.reminder_dispatcher = reminder_dispatcher
        self.reminder_scheduler = reminder_scheduler
        self.labeler = BotLabeler()

        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Регистрирует все обработчики сообщений."""

        @self.labeler.message(text="/start")
        @self.labeler.message(text="/help")
        async def handle_start_help(message: Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_id, text=message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/remind")
        async def handle_remind(message: Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_id, text=message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/cancel_reminder")
        async def handle_cancel(message: Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_id, text=message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/reminders")
        async def handle_list(message: Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_id, text=message.text or ""
            )
            await message.answer(response)

        @self.labeler.message()
        async def handle_unknown(message: Message):
            response = await self.reminder_dispatcher.dispatch(
                user_id=message.from_id, text=message.text or ""
            )
            await message.answer(response)

        # Подключаем лейблер к боту
        self.bot.labeler = self.labeler

    def _run_bot_blocking(self) -> None:
        """
        Блокирующий запуск бота.
        Этот метод должен выполняться в отдельном потоке, так как
        self.bot.run_forever() блокирует выполнение до остановки бота.
        """
        self.bot.run_forever()

    async def start(self) -> None:
        """
        Запускает планировщик и бота.
        Планировщик запускается асинхронно, а бот — в отдельном потоке
        через asyncio.to_thread, чтобы не блокировать основной цикл событий.
        """
        try:
            logger.info("VK бот запускается...")
            await self.reminder_scheduler.start()
            logger.info("Планировщик запущен, запускаем VK бота...")

            # Запускаем блокирующий метод в отдельном потоке
            await asyncio.to_thread(self._run_bot_blocking)

        except Exception:
            logger.critical("Ошибка во время запуска VK бота", exc_info=True)
        finally:
            logger.info("Останавливаем планировщик...")
            await self.reminder_scheduler.shutdown()
            logger.info("VK бот остановлен")
