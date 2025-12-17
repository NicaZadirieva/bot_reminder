# Cancel and not remind command
from app.services.reminder_service import ReminderService
from .base import BotCommand
from aiogram import types
from app.database.models import Status
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
            # ✅ Обновить ТОЛЬКО статус
            updated = await self.reminderService.cancel_reminder_by_id(
                reminder_id
            )

            if updated:
                await self.reminderScheduler.cancel_reminder_job(reminder_id)
                await message.reply(f"✅ Напоминание #{reminder_id} отменено")
            else:
                await message.reply(f"❌ Напоминание не найдено")
        
        except ValueError:
            await message.reply("❌ Неправильный ID")
        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}")