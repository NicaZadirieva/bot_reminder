# Cancel and not remind command
from .base import BotCommand
from aiogram import types

class CancelReminderCommand(BotCommand):
    async def execute(self, message: types.Message):
        pass