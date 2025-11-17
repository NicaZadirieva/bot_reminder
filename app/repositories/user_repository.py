from sqlalchemy import select
from app.repositories.postgres_repository import PostgresRepository
from app.database.models import User

class UserRepository(PostgresRepository):
    def __init__(self):
        super().__init__(User)