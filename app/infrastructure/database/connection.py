# Connect to db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.models import Base
from app.core import settings

engine = create_async_engine(settings.db.DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
