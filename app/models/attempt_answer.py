from typing import Union

from pydantic import BaseModel


class BaseAttemptAnswer(BaseModel):
    value: Union[int, str, list[int]]


class AttemptAnswerInDB(BaseAttemptAnswer):
    is_correct: bool
