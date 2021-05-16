from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument
from typing import Optional

from bson import ObjectId

from db.exceptions import DatabaseResultException
from crud.base import AbstractCRUD
from models.quiz import QuizInDB


class QuizCRUD(AbstractCRUD):
    """Describes CRUD operations for quizzes"""

    _collection_name = 'quizzes'
    _model = QuizInDB

    async def create(self, quiz_data: dict, session: Optional[AsyncIOMotorClientSession] = None) -> QuizInDB:
        """
        Insert quiz document to the DB
        :param quiz_data: quiz data in QuizInCreate format
        :param session: AsyncIOMotorClientSession to make transactions when needed
        :return: QuizInDB instance filled with quiz data
        """
        check_duplicate = await self._db[self._collection_name].find_one({'post_id': quiz_data['post_id']})
        if check_duplicate is not None:
            raise DatabaseResultException(f'There is a quiz with post id "{quiz_data["post_id"]}" already')

        row = await self._db[self._collection_name].insert_one(quiz_data)
        quiz = self._model(**quiz_data, _id=row.inserted_id)

        return quiz

    async def update(self, quiz_id: ObjectId, quiz_data: dict,
                     session: Optional[AsyncIOMotorClientSession] = None) -> QuizInDB:
        """
        Update quiz document in the DB by quiz _id
        :param quiz_id: should be valid ObjectId string
        :param quiz_data: quiz data in QuizInCreate format
        :param session: AsyncIOMotorClientSession to make transactions when needed
        :return: QuizInDB instance filled with quiz data
        """
        new_quiz = await self._db[self._collection_name].find_one_and_update(
            {'_id': quiz_id},
            {'$set': quiz_data},
            session=session,
            return_document=ReturnDocument.AFTER
        )
        if new_quiz is None:
            raise DatabaseResultException(f'There are no quizzes with ObjectId("{quiz_id}")')

        return self._model(**new_quiz)
