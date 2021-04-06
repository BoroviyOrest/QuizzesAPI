from fastapi import APIRouter, Depends

from core.dependencies import init_crud
from crud.quiz import QuizCRUD
from models.quiz import QuizInCreate, QuizInResponseFull

router = APIRouter()


@router.get('/{quiz_id}', response_model=QuizInResponseFull)
async def get_all_quizzes(quiz_id: str, crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    quiz = await crud.get_by_id(quiz_id)

    return quiz


@router.get('/', response_model=list[QuizInResponseFull])
async def get_quiz_by_id(crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    quizzes_list = await crud.get_many()

    return quizzes_list


@router.post('/', response_model=QuizInResponseFull, status_code=201)
async def create_quiz(quiz_data: QuizInCreate, crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    new_quiz = await crud.create(quiz_data)

    return new_quiz


@router.put('/{quiz_id}', response_model=QuizInResponseFull)
async def update_quiz(quiz_id: str, quiz_data: QuizInCreate, crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    new_quiz = await crud.update(quiz_id, quiz_data)

    return new_quiz


@router.delete('/{quiz_id}', status_code=204)
async def delete_quiz(quiz_id: str, crud: QuizCRUD = Depends(init_crud(QuizCRUD))):
    await crud.delete(quiz_id)

    return {'message': 'ok'}
