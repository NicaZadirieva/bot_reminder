from sqlalchemy import select
from app.models.models import Reminder as ReminderDb, Platform as PlatformDb
from sqlalchemy.ext.asyncio import AsyncSession
from .repository_interface import IRepository


class ReminderRepository(IRepository):
    def __init__(self, db_session: AsyncSession, platform: PlatformDb):
        self.db_session = db_session
        self.platform = platform
        self.model = ReminderDb

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
