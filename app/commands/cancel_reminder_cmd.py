# Cancel to remind command
from app.services.reminder_service import ReminderService
from .base import BotCommand
from aiogram import types
from typing import Any
from app.schedulers.reminder_scheduler import ReminderScheduler

class CancelReminderCommand(BotCommand):
    def __init__(self, reminderService: ReminderService, reminderScheduler: ReminderScheduler):
        super().__init__()
        self.reminderService = reminderService
        self.reminderScheduler = reminderScheduler

    async def execute(self, message: types.Message):
        try:
            # ✅ Парсить ID из команды
            # message.text = "/cancel_reminder 123"
            reminder_id = int(message.text.split(" ")[-1])
            user_id = message.from_user.id
            # ✅ Обновить ТОЛЬКО статус
            updated = await self.reminderService.cancel_reminder_by_id(
                reminder_id, user_id
            )

            if updated:
                try:
                    await self.reminderScheduler.cancel_reminder_job(reminder_id, user_id)
                    await message.reply(f"✅ Напоминание #{reminder_id} отменено")
                except e:
                    await message.reply(f"❌ Произошла ошибка. Повторите позже")
            else:
                await message.reply(f"❌ Напоминание не найдено")
        
        except ValueError:
            await message.reply("❌ Неправильный ID")
        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}")