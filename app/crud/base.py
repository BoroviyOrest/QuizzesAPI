from abc import ABC, abstractmethod
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from core.config import database_name


class AbstractCRUD(ABC):
    """Describes abstract CRUD class for database interaction"""

    _collection_name: str

    def __init__(self, client: AsyncIOMotorClient):
        self._db = client[database_name]

    @abstractmethod
    async def get_by_id(self, document_id: str) -> object:
        pass

    @abstractmethod
    async def get_many(self) -> List[BaseModel]:
        pass

    @abstractmethod
    async def create(self, document_data: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    async def update(self, document_id: str, document_data: BaseModel) -> BaseModel:
        pass

    @abstractmethod
    async def delete(self, document_id: str) -> None:
        pass
