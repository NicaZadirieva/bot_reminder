# Reminder-specific repository
from .postgres_repository import PostgresRepository
from app.infrastructure.database import ReminderDb
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import PlatformDb


class ReminderRepository(PostgresRepository):
    def __init__(self, db_session: AsyncSession, platform: PlatformDb):
        super().__init__(ReminderDb, db_session, platform)
