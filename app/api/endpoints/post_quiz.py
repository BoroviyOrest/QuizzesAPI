from fastapi import APIRouter, Depends

from core.dependencies import init_service
from models.quiz import QuizInResponsePartial
from services.quiz import QuizService

router = APIRouter()


@router.get('/{post_id}', response_model=QuizInResponsePartial)
async def get_quiz_by_post_id(post_id: int, service: QuizService = Depends(init_service(QuizService))):
    quiz = await service.get_by_post_id(post_id)

    return quiz
