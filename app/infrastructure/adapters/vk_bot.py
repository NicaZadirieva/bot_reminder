from app.core.bot import Bot
from app.presentation.vk_client import VKClient


class VkBotAdapter(Bot):
    """Адаптер, приводящий VKClient к интерфейсу Bot."""

    def __init__(self, vk_client: VKClient):
        self._vk_client = vk_client

    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        """
        Отправляет сообщение пользователю VK.

        :param chat_id: Идентификатор пользователя (peer_id).
        :param text: Текст сообщения.
        :param kwargs: Дополнительные параметры:
            - keyboard (dict): клавиатура для сообщения.
            - (в будущем можно добавить другие параметры VK API).
        """
        keyboard = kwargs.get("keyboard")
        await self._vk_client.send_message(
            user_id=chat_id, message=text, keyboard=keyboard
        )
