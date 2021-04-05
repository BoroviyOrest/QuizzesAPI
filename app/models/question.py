from typing import Optional, Union

from pydantic import BaseModel, HttpUrl, validator


class BaseQuestion(BaseModel):
    description: str
    media: Optional[HttpUrl]
    type: str
    options: Optional[list[str]]


class QuestionFull(BaseQuestion):
    answer: Union[int, str, list[int]]


class QuestionPartial(BaseQuestion):
    pass


class QuestionInCreate(BaseQuestion):
    _question_type: str  # I use private attribute, because Pydantic will use this attr otherwise

    answer: Union[int, str, list[int]]


class TextQuestionInCreate(QuestionInCreate):
    _question_type = 'text'

    answer: str


class RadioQuestionInCreate(QuestionInCreate):
    _question_type = 'radio'

    answer: int
    options: list[str]

    @validator('answer')
    def validate_answer(cls, answer: int, values: dict) -> int:
        options = values.get('options')

        if len(options) <= answer:
            raise ValueError('Answer value is greater then options list length')
        return answer


class CheckboxQuestionInCreate(QuestionInCreate):
    _question_type = 'checkbox'

    answer: list[int]
    options: list[str]

    @validator('answer')
    def validate_answer(cls, answer: list[int], values: dict) -> list[int]:
        options = values.get('options')

        for value in answer:
            if len(options) <= value:
                raise ValueError(f'Answer value {value} is greater then options list length')

        return answer
