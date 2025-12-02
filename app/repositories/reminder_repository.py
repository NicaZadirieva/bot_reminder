# Reminder-specific repository
from sqlalchemy import select
from app.repositories.postgres_repository import PostgresRepository
from app.database.models import Reminder

class ReminderRepository(PostgresRepository):
    def __init__(self):
        super().__init__(Reminder)
