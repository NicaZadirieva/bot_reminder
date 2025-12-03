# Cancel and not remind command
from .base import BotCommand
from aiogram import types
from app.repositories.base import IRepository
from entities.reminder import ReminderStatus
from typing import Any
from schedulers.reminder_scheduler import ReminderScheduler

class CancelReminderCommand(BotCommand):
    def __init__(self, repo: IRepository, session: Any, reminderScheduler: ReminderScheduler):
        super().__init__()
        self.repo = repo
        self.session = session
        self.reminderScheduler = reminderScheduler

    async def execute(self, message: types.Message):
        try:
            # ✅ Парсить ID из команды
            # message.text = "/cancel_reminder 123"
            reminder_id = int(message.text.split(" ")[-1])

            await self.reminderScheduler.cancel_reminder_job(reminder_id)
            
            # ✅ Обновить ТОЛЬКО статус
            updated = await self.repo.update(
                self.session,
                reminder_id,
                status=ReminderStatus.CANCELLED
            )
            
            if updated:
                await message.reply(f"✅ Напоминание #{reminder_id} отменено")
            else:
                await message.reply(f"❌ Напоминание не найдено")
        
        except ValueError:
            await message.reply("❌ Неправильный ID")
        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}")