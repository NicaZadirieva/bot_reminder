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
    Использует bot.loop_wrapper для управления задачами запуска/остановки.
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
        self._register_loop_tasks()
        self.bot.labeler = self.labeler

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

    def _register_loop_tasks(self) -> None:
        loop = self.bot.loop_wrapper.loop
        self._create_tasks(loop)

    async def _delayed_register(self):
        loop = asyncio.get_running_loop()
        self._create_tasks(loop)

    def _create_tasks(self, loop):
        startup_task = loop.create_task(self.reminder_scheduler.start())
        shutdown_task = loop.create_task(self.reminder_scheduler.shutdown())
        self.bot.loop_wrapper.on_startup.append(startup_task)
        self.bot.loop_wrapper.on_shutdown.append(shutdown_task)

    def start(self) -> None:
        """Запускает бота."""
        try:
            logger.info("VK бот запускается...")
            # Вся логика жизненного цикла уже зарегистрирована в loop_wrapper
            self.bot.run_forever()
            logger.info("VK бот успешно запущен")
        except Exception:
            logger.critical(
                "Ошибка во время запуска VK бота. Работа бота невозможна",
                exc_info=True,
            )
        finally:
            # Дополнительная очистка, если необходимо
            pass
