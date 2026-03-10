# Reminder-specific repository
from app.repositories.postgres_repository import PostgresRepository
from app.database import ReminderDb


class ReminderRepository(PostgresRepository):
    def __init__(self):
        super().__init__(ReminderDb)
