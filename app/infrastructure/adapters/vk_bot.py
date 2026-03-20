from vkbottle import Bot as VkBot
from app.core.bot import Bot


class VkBotAdapter(Bot):
    """Адаптер, приводящий vkbottle.Bot к интерфейсу Bot."""

    def __init__(self, vk_bot: VkBot):
        self._vk_bot = vk_bot

    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        """
        Отправляет сообщение пользователю VK.

        :param chat_id: Идентификатор пользователя (peer_id).
        :param text: Текст сообщения.
        :param kwargs: Дополнительные параметры для vk_api.messages.send
                       (например, random_id, attachment и т.д.).
        """
        await self._vk_bot.api.messages.send(peer_id=chat_id, message=text, **kwargs)
