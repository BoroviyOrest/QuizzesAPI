from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import DatabaseResultException


async def database_result_error_handler(request: Request, exc: DatabaseResultException):
    return JSONResponse(
        status_code=404,
        content={
            'message': str(exc)
        }
    )
