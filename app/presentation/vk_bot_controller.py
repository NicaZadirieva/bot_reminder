import asyncio
import logging
from typing import Dict, Any

from app.presentation.command_dispatcher import ReminderDispatcher
from app.application.services.reminder_scheduler import ReminderScheduler
from app.presentation.vk_client import VKClient

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
        """Обрабатывает событие. type=4 — новое сообщение."""
        if update.get("type") != 4:
            return

        msg_obj = update.get("object")
        if not msg_obj:
            return

        user_id = msg_obj.get("from_id")
        text = msg_obj.get("text", "")

        if not user_id or text is None:
            return

        response = await self.dispatcher.dispatch(user_id=user_id, text=text)
        if response:
            await self.client.send_message(user_id, response)

    def stop(self):
        self._running = False
