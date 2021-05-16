from abc import ABC, abstractmethod
from typing import Type, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from pydantic import BaseModel

from core.config import database_name
from db.exceptions import DatabaseResultException


class AbstractCRUD(ABC):
    """Describes abstract CRUD class for database interaction"""

    _collection_name: str
    _model: Type[BaseModel]

    def __init__(self, client: AsyncIOMotorClient):
        self._db = client[database_name]

    async def get(self, *args, **kwargs):
        """
        Retrieve document from the DB by parameters passed as key arguments
        :return: BaseModel subclass instance filled with document data
        """
        data = await self._db[self._collection_name].find_one(kwargs)

        if data is None:
            raise DatabaseResultException(f'There are no {self._collection_name} by "{kwargs}"')

        return self._model(**data)

    async def get_many(self, *args, **kwargs) -> list:
        """
        Retrieve many documents from the DB by parameters passed as key arguments
        :return: list of BaseModel subclass instance filled with document data
        """
        cursor = self._db[self._collection_name].find(kwargs)
        result = [self._model(**document) for document in await cursor.to_list(length=None)]

        return result

    @abstractmethod
    async def create(self, document_data: dict, session: Optional[AsyncIOMotorClientSession] = None) -> BaseModel:
        """
        Insert a document to the DB
        :param document_data: BaseModel subclass instance filled with document data
        :param session: AsyncIOMotorClientSession instance to make a transaction
        :return: BaseModel subclass instance filled with document data
        """
        pass

    async def delete(self, document_id: ObjectId, session: Optional[AsyncIOMotorClientSession] = None) -> None:
        """
        Delete document from the DB by _id
        :param document_id: ObjectId instance
        :param session: AsyncIOMotorClientSession instance to make a transaction
        """
        result = await self._db[self._collection_name].delete_one({'_id': document_id}, session=session)
        if result.deleted_count == 0:
            raise DatabaseResultException(f'There are no {self._collection_name} with {document_id}')
