from abc import ABC, abstractmethod
from aiogram import types

# Base command
class BotCommand(ABC):
    @abstractmethod
    async def execute(self, message: types.Message):
        pass