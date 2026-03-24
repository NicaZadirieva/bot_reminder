from abc import abstractmethod


class BaseCommandDispatcher:
    """
    Базовый класс.

    Диспетчер команд для работы с напоминаниями.
    Принимает на вход ID пользователя и текст сообщения,
    определяет команду и делегирует выполнение соответствующему use case.
    """

    @abstractmethod
    async def dispatch(self, user_id: int, text: str) -> str:
        """
        Маршрутизирует сообщение к нужной команде.

        :param user_id: ID пользователя (из Telegram / VK / и т.д.)
        :param text: полный текст сообщения (например, "/remind купить молоко | 18:00")
        :return: текст ответа для отправки пользователю
        """
        pass
