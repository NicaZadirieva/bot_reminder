import asyncio
import threading
import time
import logging
from typing import Callable, Any, Optional
from app.infrastructure.database import PlatformDb
from vkbottle import Bot
from vkbottle.bot import BotLabeler, Message
from apscheduler.schedulers.base import SchedulerNotRunningError

from app.application.utils.parsers.reminder_parser import ReminderParser
from app.infrastructure.adapters.vk_bot import VkBotAdapter
from app.presentation.command_dispatcher import ReminderDispatcher
from app.application.services.reminder_scheduler import ReminderScheduler

from app.infrastructure.repositories.reminder_repository import ReminderRepository
from app.application.services.reminder_service import ReminderService

logger = logging.getLogger(__name__)


class VkBotController:
    def __init__(
        self,
        vk_bot: Bot,
        bot_adapter: VkBotAdapter,
        reminder_parser: ReminderParser,
        session_factory: Callable[[], Any],
        timezone_str: str,
    ):
        self.bot = vk_bot
        self.bot_adapter = bot_adapter
        self.reminder_parser = reminder_parser
        self.session_factory = session_factory
        self.timezone_str = timezone_str

        self.labeler = BotLabeler()
        self._setup_handlers()
        self.bot.labeler = self.labeler

        self._scheduler_loop: Optional[asyncio.AbstractEventLoop] = None
        self._scheduler_thread: Optional[threading.Thread] = None

    def _setup_handlers(self):
        @self.labeler.message(text="/start")
        @self.labeler.message(text="/help")
        async def handle_start_help(message: Message):
            response = await self._dispatch_with_future(
                message.from_id, message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/remind")
        async def handle_remind(message: Message):
            response = await self._dispatch_with_future(
                message.from_id, message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/cancel_reminder")
        async def handle_cancel(message: Message):
            response = await self._dispatch_with_future(
                message.from_id, message.text or ""
            )
            await message.answer(response)

        @self.labeler.message(text="/reminders")
        async def handle_list(message: Message):
            response = await self._dispatch_with_future(
                message.from_id, message.text or ""
            )
            await message.answer(response)

        @self.labeler.message()
        async def handle_unknown(message: Message):
            response = await self._dispatch_with_future(
                message.from_id, message.text or ""
            )
            await message.answer(response)

    async def _dispatch_with_future(self, user_id: int, text: str) -> str:
        """Вызывает диспетчер в потоке планировщика и ждёт ответ."""
        loop = self._scheduler_loop
        if loop is None or loop.is_closed():
            return "Сервис временно недоступен, попробуйте позже."

        # Создаём future в основном потоке, выполняем в потоке планировщика
        future = asyncio.run_coroutine_threadsafe(
            self._dispatch_in_scheduler(user_id, text), loop
        )
        try:
            return await asyncio.wrap_future(future)
        except Exception as e:
            logger.error(f"Ошибка при вызове диспетчера: {e}")
            return "Произошла ошибка при обработке команды."

    async def _dispatch_in_scheduler(self, user_id: int, text: str) -> str:
        """Выполняется в цикле планировщика, использует свой экземпляр диспетчера."""
        if not hasattr(self, "_dispatcher"):
            return "Сервис ещё не готов."
        return await self._dispatcher.dispatch(user_id, text)

    def _create_services(self, session):
        repo = ReminderRepository(session, PlatformDb.VK)
        reminder_service = ReminderService(repo)
        from pytz import timezone

        tz = timezone(self.timezone_str)
        scheduler = ReminderScheduler(reminder_service, self.bot_adapter, tz)
        dispatcher = ReminderDispatcher(
            reminder_service, scheduler, self.reminder_parser
        )
        return scheduler, dispatcher

    def _run_scheduler_loop(self):
        self._scheduler_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._scheduler_loop)

        session = self.session_factory()
        try:
            scheduler, dispatcher = self._create_services(session)
            self._scheduler = scheduler
            self._dispatcher = dispatcher

            # Запускаем планировщик
            self._scheduler_loop.run_until_complete(scheduler.start())
            # Держим цикл активным, чтобы планировщик работал в фоне
            self._scheduler_loop.run_forever()
        except Exception as e:
            logger.error(f"Ошибка в потоке планировщика: {e}", exc_info=True)
        finally:
            # Останавливаем планировщик
            try:
                self._scheduler_loop.run_until_complete(scheduler.shutdown())
            except SchedulerNotRunningError:
                logger.debug("Планировщик уже остановлен")
            except Exception as e:
                logger.error(f"Ошибка при остановке планировщика: {e}", exc_info=True)
            # Закрываем сессию
            if hasattr(session, "close"):
                close_coro = session.close()
                if asyncio.iscoroutine(close_coro):
                    self._scheduler_loop.run_until_complete(close_coro)
                else:
                    close_coro()
            self._scheduler_loop.close()

    def start(self) -> None:
        try:
            logger.info("VK бот запускается...")
            self._scheduler_thread = threading.Thread(
                target=self._run_scheduler_loop, daemon=True
            )
            self._scheduler_thread.start()
            time.sleep(0.5)  # даём время на инициализацию
            logger.info("Планировщик запущен, запускаем VK бота...")
            self.bot.run_forever()
        except Exception:
            logger.critical("Ошибка во время запуска VK бота", exc_info=True)
        finally:
            logger.info("Останавливаем планировщик...")
            if self._scheduler_loop:
                self._scheduler_loop.call_soon_threadsafe(self._scheduler_loop.stop)
            if self._scheduler_thread:
                self._scheduler_thread.join()
            logger.info("VK бот остановлен")
