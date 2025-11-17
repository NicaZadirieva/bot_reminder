# Base repository

from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    """Base repo"""
    
    @abstractmethod
    async def get_by_id(self, session, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    async def get_all(self, session) -> List[T]:
        pass
    
    @abstractmethod
    async def create(self, session, obj: T) -> T:
        pass
    
    @abstractmethod
    async def update(self, session, id: int, **kwargs) -> T:
        pass
    
    @abstractmethod
    async def delete(self, session, id: int) -> bool:
        pass
