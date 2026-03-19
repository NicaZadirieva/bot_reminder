# Reminder-specific repository
from .postgres_repository import PostgresRepository
from app.infrastructure.database import ReminderDb
from sqlalchemy.ext.asyncio import AsyncSession


class ReminderRepository(PostgresRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ReminderDb, db_session)
