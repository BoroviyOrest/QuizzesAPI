from typing import List

from pydantic import BaseModel

from app.schemas.question import QuestionInResponse, QuestionInDB


class Quiz(BaseModel):
    name: str
    post_id: int
    description: str


class QuizInDB(Quiz):
    questions: List[QuestionInDB]


class QuizInResponse(Quiz):
    questions: List[QuestionInResponse]
