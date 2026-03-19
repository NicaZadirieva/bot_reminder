# PostgreSQL impl
from sqlalchemy import select
from app.infrastructure.repositories.interfaces import IRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresRepository(IRepository):
    """PostgreSQL"""

    def __init__(self, model_class, db_session: AsyncSession):
        self.model = model_class
        self.db_session = db_session

    async def get_by_id(self, id: int):
        return await self.db_session.get(self.model, id)

    async def get_all(self):
        query = select(self.model)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj):
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def update(self, id: int, **kwargs):
        obj = await self.db_session.get(self.model, id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(obj)
            return obj
        return None

    async def delete(self, id: int):
        obj = await self.db_session.get(self.model, id)
        if not obj:
            return False
        await self.db_session.delete(obj)
        await self.db_session.commit()
        return True
