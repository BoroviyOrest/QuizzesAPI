from fastapi import APIRouter, Depends

from core.dependencies import init_service
from models.attempt import AttemptInResponse, AttemptInCreate
from services.attempt import AttemptService

router = APIRouter()


@router.get('/{attempt_id}', response_model=AttemptInResponse)
async def get_attempt(attempt_id: str, service: AttemptService = Depends(init_service(AttemptService))):
    attempt = await service.get_by_id(attempt_id)

    return attempt


@router.get('/', response_model=list[AttemptInResponse])
async def get_attempts_by_quiz_id(quiz_id: str, service: AttemptService = Depends(init_service(AttemptService))):
    attempts = await service.get_by_quiz_id(quiz_id)

    return attempts


@router.post('/', response_model=AttemptInResponse, status_code=201)
async def pass_quiz(quiz_data: AttemptInCreate, service: AttemptService = Depends(init_service(AttemptService))):
    new_quiz = await service.pass_quiz(quiz_data)

    return new_quiz


@router.delete('/{attempt_id}', status_code=204)
async def delete_quiz(attempt_id: str, service: AttemptService = Depends(init_service(AttemptService))):
    await service.delete(attempt_id)

    return {'message': 'ok'}
