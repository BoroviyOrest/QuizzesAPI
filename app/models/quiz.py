from typing import List

from pydantic import BaseModel, validator

from models.question import QuestionInResponse, QuestionInCreate
from models.db import DBModelMixin


class BaseQuiz(BaseModel):
    name: str
    post_id: int
    description: str


class QuizInCreate(BaseQuiz):
    questions: list[QuestionInCreate]

    @validator('questions')
    def validate_questions(cls, questions: list[QuestionInCreate]) -> list[QuestionInCreate]:
        """
        To validate questions properly, and with alignment to OCP, we have several
        classes (syb-classes of QuestionInCreate class) which describe specific
        validation of the "options" and "answer" fields depending on the "type" of the question.
        Because of that we should have some check on which question type user wants to create and to give
        it an appropriate validation. I decided to make a mapper, that will generate automatically,
        no matter how many new question types we will have in the future. It generates from __subclasses__ of the
        QuestionInCreate class, which is a base class for all question types and takes _question_type attribute of each
        class to match it with question type, that user filled in.
        :param questions: list of QuestionInCreate instances
        :return: list of QuestionInCreate sub classes instances
        """
        mapper = {model_class._question_type: model_class for model_class in QuestionInCreate.__subclasses__()}

        validated_questions = []
        for question in questions:
            try:
                model = mapper[question.type]
                validated_questions.append(model(**question.dict()))
            except KeyError:
                raise ValueError(f'Question type {question.type} is not in list: {mapper.keys()}')

        return validated_questions


class QuizInDB(QuizInCreate, DBModelMixin):
    pass


class QuizInResponse(BaseQuiz, DBModelMixin):
    questions: List[QuestionInResponse]
