from .base import BotCommand
from aiogram import types

class StartCommand(BotCommand):
    async def execute(self, message: types.Message):
        await message.answer(
        "\n".join([
            "👋 Привет! Я бот-напоминалка.\n",
            "📝 Основные команды:",
            "/remind - Создать напоминание",
            "/reminders - Показать все напоминания",
            "/cancel_reminder - Отменить напоминание",
            "/help - Справка!"
        ])
        
    )