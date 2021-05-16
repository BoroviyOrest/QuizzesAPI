from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from crud.attempt import AttemptCRUD
from crud.quiz import QuizCRUD
from models.attempt import AttemptInDB, AttemptInCreate


class AttemptService:
    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._quiz_crud = QuizCRUD(client)
        self._attempt_crud = AttemptCRUD(client)

    async def get_by_id(self, attempt_id: str) -> AttemptInDB:
        """
        Get attempt data by document ID
        :param attempt_id: should be valid ObjectId string
        :return: AttemptInDB instance filled with attempt data
        """
        return await self._attempt_crud.get(id=ObjectId(attempt_id))

    async def get_by_quiz_id(self, quiz_id: str) -> list[AttemptInDB]:
        """
        Get all attempts by quiz
        :param quiz_id: should be valid ObjectId string
        :return: list of AttemptInDB instances filled with attempt data
        """
        return await self._attempt_crud.get_many(quiz_id=quiz_id)

    async def pass_quiz(self, attempt: AttemptInCreate) -> AttemptInDB:
        """
        Check all answers in attempt and save it to the DB
        :param attempt: AttemptInCreate instance filled with attempt data
        :return: AttemptInDB instance filled with attempt data
        """
        quiz = await self._quiz_crud.get(_id=attempt.quiz_id)
        attempt_data = attempt.dict()

        score = 0
        for question, answer in zip(quiz.questions, attempt_data['answers']):
            answer['is_correct'] = question.answer == answer['value']
            score += int(answer['is_correct'])

        attempt_data['total_score'] = score

        return await self._attempt_crud.create(attempt_data)

    async def delete(self, attempt_id: str) -> None:
        """
        Remove attempt
        :param attempt_id: should be valid ObjectId string
        :return: None
        """
        await self._attempt_crud.delete(ObjectId(attempt_id))
