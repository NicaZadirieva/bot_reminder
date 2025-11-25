# Create remind
from .base import BotCommand
from app.parsers.reminder_parser import ReminderParser
from app.repositories.base import IRepository
from aiogram import types
from typing import Optional, List, Any

class CreateReminderCommand(BotCommand):
    def __init__(self, repo: IRepository, session: Any):
        super().__init__()
        self.parser = ReminderParser()
        self.repo = repo
        self.session = session

    async def execute(self, message: types.Message):
        # TODO: подумать как заменить \remind, replace
        user_text = message.text.replace("\remind", "")
        try:
            reminder = self.parser.parse(user_text, message.from_user.id)
            await self.repo.create(self.sesion, reminder);
        except:
            message.answer("Формат данных не соответсвует команде")

