import asyncio
import logging
from typing import Dict, Any

from app.commands.dispatchers.remind_dispatcher import ReminderDispatcher
from app.services.reminder_scheduler import ReminderScheduler
from app.controllers.vk.vk_client import VKClient

logger = logging.getLogger(__name__)


class VkBotController:
    def __init__(
        self,
        vk_client: VKClient,
        reminder_dispatcher: ReminderDispatcher,
        reminder_scheduler: ReminderScheduler,
    ):
        self.client = vk_client
        self.dispatcher = reminder_dispatcher
        self.scheduler = reminder_scheduler
        self._running = True

    async def start(self) -> None:
        """Запускает планировщик и цикл обработки longpoll."""
        logger.info("VK бот запускается...")
        await self.scheduler.start()

        try:
            lp_data = await self.client.get_longpoll_server()
            server = lp_data.get("server")
            if not server:
                logger.error(f"Invalid LongPoll response: {lp_data}")
                raise RuntimeError("LongPoll server not found")
            key = lp_data["key"]
            ts = lp_data["ts"]
            logger.info(f"LongPoll подключён. server={server}, key={key}, ts={ts}")

            while self._running:
                events = await self.client.poll_events(server, key, ts)
                if "failed" in events:
                    # Обработка ошибок longpoll
                    if events.get("failed") == 1:
                        ts = events.get("ts", ts)
                    else:
                        lp_data = await self.client.get_longpoll_server()
                        server = lp_data["server"]
                        key = lp_data["key"]
                        ts = lp_data["ts"]
                    continue

                ts = events["ts"]
                for update in events.get("updates", []):
                    await self._handle_update(update)

        except asyncio.CancelledError:
            logger.info("LongPoll цикл отменён")
        except Exception as e:
            logger.critical(f"Ошибка в longpoll: {e}", exc_info=True)
        finally:
            await self.scheduler.shutdown()
            await self.client.close()
            logger.info("VK бот остановлен")

    async def _handle_update(self, update: Dict[str, Any]) -> None:
        logger.debug(update)
        if update.get("type") != "message_new":
            return

        obj = update.get("object")
        if not obj:
            return

        message = obj.get("message")
        if not message:
            return

        user_id = message.get("from_id")
        text = message.get("text", "")

        if not user_id or text is None:
            return

        # Разбор команды (первое слово без "/")
        command = None
        if text.startswith("/"):
            parts = text.split(maxsplit=1)
            command = parts[0][1:].lower()  # убираем '/'

        # Диспетчеризация по командам
        if command == "start" or command == "help":
            await self._handle_start_help(user_id, text)
        elif command == "remind":
            await self._handle_remind(user_id, text)
        elif command == "cancel_reminder":
            await self._handle_cancel_reminder(user_id, text)
        elif command == "reminders":
            await self._handle_list_reminders(user_id, text)
        else:
            # Любое сообщение без команды или неизвестная команда
            await self._handle_unknown(user_id, text)

    # --- Обработчики команд ---
    async def _handle_start_help(self, user_id: int, text: str) -> None:
        """Обработчик /start и /help."""
        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    async def _handle_remind(self, user_id: int, text: str) -> None:
        """Обработчик /remind."""
        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    async def _handle_cancel_reminder(self, user_id: int, text: str) -> None:
        """Обработчик /cancel_reminder."""
        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    async def _handle_list_reminders(self, user_id: int, text: str) -> None:
        """Обработчик /reminders."""
        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    async def _handle_unknown(self, user_id: int, text: str) -> None:
        """Обработчик всех остальных сообщений."""
        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    def stop(self):
        self._running = False
