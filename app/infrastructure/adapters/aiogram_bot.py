from aiogram import Bot as AiogramBot
from app.shared.abstracts.bot import Bot


class AiogramBotAdapter(Bot):
    """Адаптер, приводящий aiogram.Bot к интерфейсу Bot."""

    def __init__(self, aiogram_bot: AiogramBot):
        self._aiogram_bot = aiogram_bot

    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        # При необходимости можно пробросить дополнительные параметры (parse_mode, reply_markup и т.д.)
        await self._aiogram_bot.send_message(chat_id=chat_id, text=text, **kwargs)
