from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
from app.infrastructure.database import PlatformDb
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class IRepository(ABC, Generic[T]):
    """Base repo"""

    platform: PlatformDb

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def create(self, obj: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: int, **kwargs) -> T:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
