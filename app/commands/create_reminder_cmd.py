# Create remind
from .base import BotCommand
from aiogram import types

class CreateReminderCommand(BotCommand):
    async def execute(self, message: types.Message):
        pass