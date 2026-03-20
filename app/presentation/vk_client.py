import json
import logging
import random
import time
from typing import Dict, Optional, Any
from aiohttp import ClientSession, ClientTimeout
from app.core.settings import settings

logger = logging.getLogger(__name__)


class VKClient:
    """
    Асинхронный клиент для VK API.
    Поддерживает отправку сообщений и получение событий через LongPoll.
    """

    def __init__(self, token: str, version: str = "5.199"):
        self.token = token
        self.version = version
        self.api_url = "https://api.vk.com/method/"
        self.session: Optional[ClientSession] = None
        self._timeout = ClientTimeout(total=30)

    async def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Выполняет запрос к VK API."""
        if self.session is None:
            self.session = ClientSession(timeout=self._timeout)

        url = f"{self.api_url}{method}"
        params.update({"access_token": self.token, "v": self.version})

        async with self.session.post(url, data=params) as resp:
            data = await resp.json()
            if "error" in data:
                error = data["error"]
                logger.error(f"VK API error: {error}")
                raise Exception(f"VK API error: {error.get('error_msg', 'unknown')}")
            return data.get("response", {})

    def _generate_random_id(self) -> int:
        """Генерирует уникальный random_id для отправки сообщения."""
        return int(time.time() * 1000) + random.randint(0, 1000)

    async def send_message(
        self, user_id: int, message: str, keyboard: Optional[Dict] = None
    ) -> Optional[int]:
        """Отправляет сообщение пользователю."""
        params = {
            "user_id": user_id,
            "message": message,
            "random_id": self._generate_random_id(),
        }
        if keyboard:
            params["keyboard"] = json.dumps(keyboard, ensure_ascii=False)

        try:
            resp = await self._request("messages.send", params)
            logger.info(f"Message sent to {user_id}, response: {resp}")
            return resp
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")
            return None

    async def get_longpoll_server(self) -> Dict[str, Any]:
        """Получает данные для подключения к LongPoll."""
        return await self._request(
            "groups.getLongPollServer", {"group_id": settings.vk_app.VK_GROUP_ID}
        )

    async def poll_events(
        self, server: str, key: str, ts: int, wait: int = 25
    ) -> Dict[str, Any]:
        """Запрашивает события с LongPoll сервера."""
        url = f"https://{server}?act=a_check&key={key}&ts={ts}&wait={wait}"
        async with self.session.get(url) as resp:
            return await resp.json()

    async def close(self):
        """Закрывает сессию aiohttp."""
        if self.session:
            await self.session.close()
