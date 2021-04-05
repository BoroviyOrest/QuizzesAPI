from fastapi import APIRouter, Request, Depends

from core.dependencies import init_crud
from crud.quiz import QuizCRUD
from models.quiz import QuizInResponsePartial

router = APIRouter()


@router.get('/', response_model=QuizInResponsePartial)
async def get_quiz_by_post_id(post_id: int, crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    quiz = await crud.get_by_post_id(post_id)

    return quiz
