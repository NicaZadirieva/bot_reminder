import asyncio
from app.database.connection import init_db, async_session
from app.database.models import User, Reminder

async def main():
    await init_db()
    print("✅ БД инициализирована!")

asyncio.run(main())