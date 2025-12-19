 # Business logics
from app.mappers.from_entity_to_model import from_entity_to_model
from app.mappers.from_model_to_entity import from_model_to_entity
from app.repositories.reminder_repository import ReminderRepository
from typing import Any
from typing import Optional, List, Any
from datetime import datetime, timedelta, timezone as dt_timezone
from pytz import timezone

from app.entities.reminder import Reminder as ReminderEntity, ReminderStatus as ReminderStatusEntity, RepeatedValue as RepeatedValueEntity, Priority as PriorityEntity
from app.database.models import Reminder as ReminderDb, RepeatedValue as RepeatedValueDb, Status as ReminderStatusDb, Priority as PriorityDb

from app.utils.Utils import Utils
import logging
logger = logging.getLogger(__name__)

class ReminderService:
    def __init__(self, repo: ReminderRepository, dbSession: Any):
        self.reminderRepo = repo
        self.dbSession = dbSession

    async def check_if_reminder_exists(self, id: int, user_id: int) -> bool:
        reminderDb = await self.reminderRepo.get_by_id(self.dbSession, id)
        if reminderDb.telegram_id != user_id:
            # напоминание не принадлежит пользователю
            return False
        return not (reminderDb is None)

    def filter_reminders_by_user(self, reminders: List[ReminderDb], user_id: int) -> List[ReminderEntity]:
        return [from_model_to_entity(r) for r in reminders if r.telegram_id == user_id]

    async def get_all_reminders(self, user_id: int) -> List[ReminderEntity]:
        all_reminders = await self.reminderRepo.get_all(self.dbSession)
        return self.filter_reminders_by_user(all_reminders, user_id)

    async def get_all_active_reminders(self) -> List[ReminderEntity]:
        # 1️⃣ Получить ВСЕ напоминания
        all_reminders = await self.reminderRepo.get_all(self.dbSession)
 
        # 2️⃣ Отфильтровать АКТИВНЫЕ
        active = [r for r in all_reminders if r.status == ReminderStatusDb.ACTIVE]
            
        # 3️⃣ Для ONCE - отфильтровать БУДУЩИЕ (не прошедшие)
        now = Utils.get_now()
        to_schedule = [
                r for r in active 
                if r.repeated_value != RepeatedValueDb.ONCE or Utils._make_aware(r.remind_at) > now
        ]
        return [from_model_to_entity(r) for r in to_schedule]

    async def cancel_reminder_by_id(self, id: int, user_id: Optional[int]) -> ReminderEntity:
        if user_id is None:
            reminderDb = await self.reminderRepo.update(
               self.dbSession,
               id,
               status=ReminderStatusDb.CANCELLED
            )
            return from_model_to_entity(reminderDb)
        else:
            is_reminder_exists = await self.check_if_reminder_exists(id, user_id)
            if is_reminder_exists:
                reminderDb = await self.reminderRepo.update(
                   self.dbSession,
                   id,
                   status=ReminderStatusDb.CANCELLED
                )
                return from_model_to_entity(reminderDb)
            else:
                return None


    async def create_reminder(self, reminder: ReminderEntity) -> ReminderEntity:
        reminderDb = await self.reminderRepo.create(self.dbSession, from_entity_to_model(reminder));
        return from_model_to_entity(reminderDb)

