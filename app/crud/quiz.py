from pymongo import ReturnDocument
from typing import Optional

from bson import ObjectId

from core.exceptions import DatabaseResultException
from crud.base import AbstractCRUD
from models.quiz import QuizInDB, QuizInCreate


class QuizCRUD(AbstractCRUD):
    """Describes CRUD operations for quizzes"""

    _collection_name = 'quizzes'

    async def get_by_id(self, quiz_id: str) -> Optional[QuizInDB]:
        """
        Retrieve quiz document from the DB by quiz _id
        :param quiz_id: should be valid ObjectId string
        :return: QuizInDB instance filled with quiz data
        """
        quiz = await self._db[self._collection_name].find_one(ObjectId(quiz_id))
        if quiz is None:
            raise DatabaseResultException(f'There are no quizzes with ObjectId("{quiz_id}")')

        return QuizInDB(**quiz)

    async def get_by_post_id(self, post_id: int) -> Optional[QuizInDB]:
        """
        Retrieve quiz document from the DB by post id
        :param post_id: Post id from other microservice
        :return: QuizInDB instance filled with quiz data
        """
        quiz = await self._db[self._collection_name].find_one({'post_id': post_id})
        if quiz is None:
            raise DatabaseResultException(f'There are no quizzes by post id "{post_id}"')

        return QuizInDB(**quiz)

    async def get_many(self) -> list[QuizInDB]:
        """
        Retrieve all quizzes
        :return: list of QuizInDB instances filled with quiz data
        """
        cursor = self._db[self._collection_name].find()
        quizzes = [QuizInDB(**document) for document in await cursor.to_list(length=None)]

        return quizzes

    async def create(self, quiz_data: QuizInCreate) -> QuizInDB:
        """
        Insert quiz document to the DB
        :param quiz_data: QuizInCreate instance filled with quiz data
        :return: QuizInDB instance filled with quiz data
        """
        row = await self._db[self._collection_name].insert_one(quiz_data.dict())
        quiz = QuizInDB(**quiz_data.dict(), _id=row.inserted_id)

        return quiz

    async def update(self, quiz_id: str, quiz_data: QuizInCreate) -> QuizInDB:
        """
        Update quiz document in the DB by quiz _id
        :param quiz_id: should be valid ObjectId string
        :param quiz_data: QuizInCreate instance filled with quiz data
        :return: QuizInDB instance filled with quiz data
        """
        new_quiz = await self._db[self._collection_name].find_one_and_update(
            {'_id': ObjectId(quiz_id)},
            {'$set': quiz_data.dict()},
            return_document=ReturnDocument.AFTER
        )
        if new_quiz is None:
            raise DatabaseResultException(f'There are no quizzes with ObjectId("{quiz_id}")')

        return QuizInDB(**new_quiz)

    async def delete(self, quiz_id: str) -> None:
        """
        Delete quiz document from the DB by quiz _id
        :param quiz_id: should be valid ObjectId string
        """
        result = await self._db[self._collection_name].delete_one({'_id': ObjectId(quiz_id)})
        if result.deleted_count == 0:
            raise DatabaseResultException(f'There are no quizzes with ObjectId("{quiz_id}")')
