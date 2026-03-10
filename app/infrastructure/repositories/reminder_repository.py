# Reminder-specific repository
from .postgres_repository import PostgresRepository
from app.infrastructure.database import ReminderDb


class ReminderRepository(PostgresRepository):
    def __init__(self):
        super().__init__(ReminderDb)
