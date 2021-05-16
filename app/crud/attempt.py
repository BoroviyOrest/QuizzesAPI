from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession

from crud.base import AbstractCRUD
from models.attempt import AttemptInDB


class AttemptCRUD(AbstractCRUD):
    """Describes CRUD operations for quiz attempts"""
    _collection_name = 'attempts'
    _model = AttemptInDB

    async def create(self, attempt_data: dict,
                     session: Optional[AsyncIOMotorClientSession] = None) -> AttemptInDB:
        """
        Create attempt document in the DB by given data
        :param attempt_data:
        :param session: AsyncIOMotorClientSession to make transactions when needed
        :return: AttemptInDB instance filled with attempt data
        """
        row = await self._db[self._collection_name].insert_one(attempt_data, session=session)
        attempt = self._model(**attempt_data, _id=row.inserted_id)

        return attempt

    async def delete_many(self, attempt_ids: list[ObjectId],
                          session: Optional[AsyncIOMotorClientSession] = None) -> int:
        """
        Delete attempt document from the DB by attempt _id
        :param attempt_ids: should be valid ObjectId string
        :param session: AsyncIOMotorClientSession to make transactions when needed
        :return: number of removed documents
        """
        result = await self._db[self._collection_name].delete_many({'_id': {'$in': attempt_ids}}, session=session)

        return result.deleted_count
