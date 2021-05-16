from fastapi import APIRouter, Depends

from core.dependencies import init_service
from models.quiz import QuizInCreate, QuizInResponseFull
from services.quiz import QuizService

router = APIRouter()


@router.get('/{quiz_id}', response_model=QuizInResponseFull)
async def get_quiz_by_id(quiz_id: str, service: QuizService = Depends(init_service(QuizService))):
    quiz = await service.get_by_id(quiz_id)

    return quiz


@router.get('/', response_model=list[QuizInResponseFull])
async def get_all_quizzes(service: QuizService = Depends(init_service(QuizService))):
    quizzes_list = await service.get_all()

    return quizzes_list


@router.post('/', response_model=QuizInResponseFull, status_code=201)
async def create_quiz(quiz_data: QuizInCreate, service: QuizService = Depends(init_service(QuizService))):
    new_quiz = await service.create(quiz_data)

    return new_quiz


@router.put('/{quiz_id}', response_model=QuizInResponseFull)
async def update_quiz(quiz_id: str, quiz_data: QuizInCreate, service: QuizService = Depends(init_service(QuizService))):
    new_quiz = await service.update(quiz_id, quiz_data)

    return new_quiz


@router.delete('/{quiz_id}', status_code=204)
async def delete_quiz(quiz_id: str, service: QuizService = Depends(init_service(QuizService))):
    await service.delete(quiz_id)

    return {'message': 'ok'}
