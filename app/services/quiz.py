from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from crud.attempt import AttemptCRUD
from crud.quiz import QuizCRUD
from db.exceptions import DatabaseResultException
from models.quiz import QuizInDB, QuizInCreate


class QuizService:
    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._quiz_crud = QuizCRUD(client)
        self._attempt_crud = AttemptCRUD(client)

    async def get_by_id(self, quiz_id: str) -> QuizInDB:
        """
        Get quiz by id
        :param quiz_id: should be valid ObjectId string
        :return: QuizInDB instance filled with quiz data
        """
        return await self._quiz_crud.get(id=ObjectId(quiz_id))

    async def get_by_post_id(self, post_id: int) -> QuizInDB:
        """
        Get a quiz by post id
        :param post_id: int
        :return: QuizInDB instance filled with quiz data
        """
        return await self._quiz_crud.get(post_id=post_id)

    async def get_all(self) -> list[QuizInDB]:
        """
        Get all quizzes
        :return: QuizInDB instance filled with quiz data
        """
        return await self._quiz_crud.get_many()

    async def create(self, quiz_data: QuizInCreate) -> QuizInDB:
        """
        Insert quiz document to the DB
        :param quiz_data: QuizInCreate instance filled with quiz data
        :return: QuizInDB instance filled with quiz data
        """
        return await self._quiz_crud.create(quiz_data.dict())

    async def update(self, quiz_id: str, quiz_data: QuizInCreate) -> QuizInDB:
        """
        Update quiz document in the DB by quiz _id
        :param quiz_id: should be valid ObjectId string
        :param quiz_data: QuizInCreate instance filled with quiz data
        :return: QuizInDB instance filled with quiz data
        """
        return await self._quiz_crud.update(
            quiz_id=ObjectId(quiz_id),
            quiz_data=quiz_data.dict()
        )

    async def delete(self, quiz_id: str) -> None:
        """
        Delete quiz document from the DB by quiz _id and cascade delete attempts
        :param quiz_id: should be valid ObjectId string
        """
        quiz_id = ObjectId(quiz_id)
        attempts_to_delete = await self._attempt_crud.get_many(quiz=quiz_id)
        id_list = [x.id for x in attempts_to_delete]

        async with await self._client.start_session() as session:
            session.start_transaction()
            try:
                await self._attempt_crud.delete_many(id_list, session=session)
                await self._quiz_crud.delete(quiz_id, session=session)
                session.commit_transaction()
            except (PyMongoError, DatabaseResultException):
                session.abort_transaction()
                raise
