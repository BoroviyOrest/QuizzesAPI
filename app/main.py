from fastapi import FastAPI

from api.api import api_router
from core.events import on_startup_handler, on_shutdown_handler
from core.exception_handlers import database_result_error_handler
from core.exceptions import DatabaseResultException


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler('startup', on_startup_handler(application))
    application.add_event_handler('shutdown', on_shutdown_handler(application))

    application.include_router(api_router)
    application.exception_handler(DatabaseResultException)(database_result_error_handler)

    return application


app = get_application()
