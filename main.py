import asyncio

from app.database.models import Reminder
from app.repositories.reminder_repository import ReminderRepository
from app.database.connection import async_session
from datetime import datetime, timedelta

reminder_repo = ReminderRepository()


async def main():
    async with async_session() as session:
        reminder = await reminder_repo.create(session, Reminder(text = "Напоминание", remind_at=datetime.now() + timedelta(hours=2), telegram_id=12345))

        reminder = await reminder_repo.get_by_id(session, 1)
    
        reminder = await reminder_repo.get_all(session)

        reminder = await reminder_repo.update(session, 1, text="Другое напоминание")

        #await user_repo.delete(session, 1)

asyncio.run(main())