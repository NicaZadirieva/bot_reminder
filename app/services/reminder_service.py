# Business logics
from app.utils.mappers.reminder import from_db_to_domain, from_domain_to_db
from app.repositories import ReminderRepository
from typing import Optional, List

from app.domain import Reminder
from app.entities import ReminderDb, RepeatedValueDb, StatusDb


from app.utils.TimeUtils import TimeUtils
import logging

logger = logging.getLogger(__name__)


class ReminderService:
    def __init__(self, repo: ReminderRepository):
        self.reminderRepo = repo

    async def check_if_reminder_exists(self, id: int, user_id: int) -> bool:
        reminderDb = await self.reminderRepo.get_by_id(id)
        if reminderDb and reminderDb.user_id != user_id:
            # напоминание не принадлежит пользователю
            return False
        return reminderDb is not None

    def __filter_reminders_by_user__(
        self, reminders: List[ReminderDb], user_id: int
    ) -> List[Reminder]:
        return [from_db_to_domain(r) for r in reminders if r.user_id == user_id]

    async def get_all_reminders(self, user_id: int) -> List[Reminder]:
        all_reminders = await self.reminderRepo.get_all()
        return self.__filter_reminders_by_user__(all_reminders, user_id)

    async def get_all_active_reminders(self) -> List[Reminder]:
        # 1️ Получить ВСЕ напоминания
        all_reminders = await self.reminderRepo.get_all()

        # 2️ Отфильтровать АКТИВНЫЕ
        active = [r for r in all_reminders if r.status == StatusDb.ACTIVE]

        # 3️ Для ONCE - отфильтровать БУДУЩИЕ (не прошедшие)
        now = TimeUtils.get_now()
        to_schedule = [
            r
            for r in active
            if r.repeated_value != RepeatedValueDb.ONCE
            or TimeUtils._make_aware(r.remind_at) > now
        ]
        return [from_db_to_domain(r) for r in to_schedule]

    async def __change_status_by_id__(
        self, id: int, user_id: Optional[int], status: StatusDb
    ) -> Reminder | None:
        if user_id is None:
            reminderDb = await self.reminderRepo.update(id, status=status)
            if reminderDb is not None:
                return from_db_to_domain(reminderDb)
            else:
                return None
        else:
            is_reminder_exists = await self.check_if_reminder_exists(id, user_id)
            if is_reminder_exists:
                reminderDb = await self.reminderRepo.update(id, status=status)
                if reminderDb is not None:
                    return from_db_to_domain(reminderDb)
                else:
                    return None
            else:
                return None

    async def cancel_reminder_by_id(
        self, id: int, user_id: Optional[int]
    ) -> Reminder | None:
        return await self.__change_status_by_id__(id, user_id, StatusDb.CANCELLED)

    async def complete_reminder_by_id(
        self, id: int, user_id: Optional[int]
    ) -> Reminder | None:
        return await self.__change_status_by_id__(id, user_id, StatusDb.COMPLETED)

    async def create_reminder(self, reminder: Reminder) -> Reminder:
        reminderDb = await self.reminderRepo.create(from_domain_to_db(reminder))
        return from_db_to_domain(reminderDb)

    async def is_completed_reminder(self, reminder_id: int, user_id: int):
        reminderDb = await self.reminderRepo.get_by_id(reminder_id)
        return (
            reminderDb
            and reminderDb.status == StatusDb.COMPLETED
            and reminderDb.user_id == user_id
        )
