from app.core import Bot
from app.controllers import VKClient


class VkBotAdapter(Bot):
    def __init__(self, vk_client: VKClient):
        self._vk_client = vk_client

    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        """Отправляет сообщение через VKClient."""
        keyboard = kwargs.get("keyboard")
        await self._vk_client.send_message(
            user_id=chat_id, message=text, keyboard=keyboard
        )
