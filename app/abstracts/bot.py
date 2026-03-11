from abc import ABC, abstractmethod


class Bot(ABC):
    """Абстракция бота для отправки сообщений."""

    @abstractmethod
    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        """Отправить текстовое сообщение в указанный чат."""
        pass
