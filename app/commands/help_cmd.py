from .base import BotCommand
from aiogram import types

class HelpCommand(BotCommand):
    async def execute(self, message: types.Message):
        await message.answer(f'''
            /remind <текст> | <время> [| приоритет] [| повтор] Создать новое напоминание
            Примеры /remind:
                /remind Купить молоко | 18:00

                /remind Встреча с командой | завтра 15:30

                /remind Позвонить маме | через 2 часа

                /remind Рабочая встреча | 09:00 | HIGH | daily

                /remind Купить подарок | 2024-11-20 19:00 | MEDIUM | once
            /reminders Показать все ваши напоминания
            /cancel_reminder <ID> Отменить напоминание по ID

        '''
    )