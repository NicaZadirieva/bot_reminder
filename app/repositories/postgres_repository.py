# PostgreSQL impl
from sqlalchemy import select
from app.repositories.base import IRepository

class PostgresRepository(IRepository):
    """PostgreSQL"""
    
    def __init__(self, model_class):
        self.model = model_class
    
    async def get_by_id(self, session, id: int):
        return await session.get(self.model, id)

    async def get_by_telegram_id(self, session, telegram_id: int):
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_all(self, session):
        query = select(self.model)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def create(self, session, obj):
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    async def update(self, session, id: int, **kwargs):
        obj = await session.get(self.model, id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
            return obj
        return None
    
    async def delete(self, session, id: int):
        obj = await session.get(self.model, id)
        if not obj:
            return False
        await session.delete(obj)
        await session.commit()
        return True

