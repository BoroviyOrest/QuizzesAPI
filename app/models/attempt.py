from bson import ObjectId
from pydantic import BaseModel, UUID4

from models.attempt_answer import BaseAttemptAnswer, AttemptAnswerInDB
from models.db import PyObjectId, DBModelMixin


class BaseAttempt(BaseModel):
    user: UUID4
    quiz_id: PyObjectId
    answers: list[BaseAttemptAnswer]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class AttemptInCreate(BaseAttempt):
    pass


class AttemptInDB(BaseAttempt, DBModelMixin):
    answers: list[AttemptAnswerInDB]
    total_score: int


class AttemptInResponse(AttemptInDB):
    pass
