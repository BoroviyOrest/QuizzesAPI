from fastapi import APIRouter, Request

from crud.quiz import QuizCRUD
from models.quiz import QuizInResponsePartial

router = APIRouter()


@router.get('/', response_model=QuizInResponsePartial)
async def get_quiz(request: Request, post_id: int):
    crud = QuizCRUD(request.app.state.mongodb)
    quiz = await crud.get_by_post_id(post_id)

    return quiz
