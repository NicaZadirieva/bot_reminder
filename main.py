import asyncio

from app.database.models import User
from app.repositories.user_repository import UserRepository
from app.database.connection import async_session

user_repo = UserRepository()


async def main():
    async with async_session() as session:
        #user = await user_repo.create(session, User(username="John", telegram_id=12345))

        user = await user_repo.get_by_id(session, 2)
    
        users = await user_repo.get_all(session)

        user = await user_repo.update(session, 2, username="Jane")

        #await user_repo.delete(session, 1)

asyncio.run(main())