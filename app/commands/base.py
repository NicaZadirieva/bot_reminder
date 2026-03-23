from abc import ABC, abstractmethod
from typing import Any, Optional


# Base command
class CommandUseCase(ABC):
    @abstractmethod
    async def execute(self, user_id: int, args: Optional[str], **kwargs) -> Any:
        """Выполнить команду.
        :param user_id: ID пользователя
        :param args: строка аргументов (после команды)
        :param kwargs: дополнительные данные (например, имя пользователя, сообщение)
        :return: результат (текст ответа, клавиатура и т.п.)
        """
        pass
