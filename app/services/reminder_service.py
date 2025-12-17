 # Business logics
from app.repositories.reminder_repository import ReminderRepository
from typing import Any
from app.database.models import Reminder, RepeatedValue, Status
from typing import Optional, List, Any
from datetime import datetime, timedelta, timezone as dt_timezone
from pytz import timezone

from app.utils.Utils import Utils
import logging
logger = logging.getLogger(__name__)

class ReminderService:
    def __init__(self, repo: ReminderRepository, dbSession: Any):
        self.reminderRepo = repo
        self.dbSession = dbSession

    async def check_if_reminder_exists(self, id: int, user_id: int):
        reminder = await self.reminderRepo.get_by_id(self.dbSession, id)
        if reminder.telegram_id != user_id:
            # напоминание не принадлежит пользователю
            return False
        return reminder is None

    async def get_all_reminders(self, user_id: int):
        all_reminders = await self.reminderRepo.get_all(self.dbSession)
        return self.filter_reminders_by_user(all_reminders, user_id)

    async def get_all_active_reminders(self):
        # 1️⃣ Получить ВСЕ напоминания
        all_reminders = await self.reminderRepo.get_all(self.dbSession)
 
        # 2️⃣ Отфильтровать АКТИВНЫЕ
        active = [r for r in all_reminders if r.status == Status.ACTIVE]
            
        # 3️⃣ Для ONCE - отфильтровать БУДУЩИЕ (не прошедшие)
        now = Utils.get_now()
        to_schedule = [
                r for r in active 
                if r.repeated_value != RepeatedValue.ONCE or Utils._make_aware(r.remind_at) > now
        ]
        return to_schedule

    async def cancel_reminder_by_id(self, id: int):
        return await self.reminderRepo.update(
           self.dbSession,
           id,
           status=Status.COMPLETED
        )


    async def create_reminder(self, reminder: Reminder):
        return await self.reminderRepo.create(self.session, reminder);

    def filter_reminders_by_user(self, reminders, user_id: int):
        return [r for r in reminders if r.telegram_id == user_id]