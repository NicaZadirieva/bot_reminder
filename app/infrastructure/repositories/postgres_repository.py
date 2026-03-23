# PostgreSQL impl
from sqlalchemy import select
from app.infrastructure.repositories.interfaces import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import PlatformDb


class PostgresRepository(IRepository):
    """PostgreSQL"""

    def __init__(self, model_class, db_session: AsyncSession, platform: PlatformDb):
        super().__init__(platform)
        self.model = model_class
        self.db_session = db_session

    async def get_by_id(self, id: int):
        """Получение записи по id с проверкой платформы."""
        stmt = select(self.model).where(
            self.model.id == id, self.model.platform == self.platform
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self):
        """Получение всех записей только для текущей платформы."""
        stmt = select(self.model).where(self.model.platform == self.platform)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj):
        """Создание записи: платформа принудительно устанавливается из репозитория."""
        obj.platform = self.platform  # гарантируем, что платформа соответствует
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def update(self, id: int, **kwargs):
        """Обновление записи с проверкой принадлежности платформе."""
        stmt = select(self.model).where(
            self.model.id == id, self.model.platform == self.platform
        )
        result = await self.db_session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(obj)
            return obj
        return None

    async def delete(self, id: int):
        """Удаление записи с проверкой принадлежности платформе."""
        stmt = select(self.model).where(
            self.model.id == id, self.model.platform == self.platform
        )
        result = await self.db_session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            return False
        await self.db_session.delete(obj)
        await self.db_session.commit()
        return True
