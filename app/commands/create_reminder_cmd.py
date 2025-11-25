# Create remind
from .base import BotCommand
from app.parsers.reminder_parser import ReminderParser
from aiogram import types

class CreateReminderCommand(BotCommand):
    def __init__(self):
        super().__init__()
        self.parser = ReminderParser()

    async def execute(self, message: types.Message):
        user_text = message.text.replace("\remind", "")
        try:
            reminder = self.parser.parse(user_text, message.from_user.id)
            # TODO: создать в бд
        except:
            message.answer("Формат данных не соответсвует команде")

