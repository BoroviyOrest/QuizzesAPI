from fastapi import FastAPI

from api.api import api_router
from core.events import on_startup_handler, on_shutdown_handler


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler('startup', on_startup_handler(application))
    application.add_event_handler('shutdown', on_shutdown_handler(application))

    application.include_router(api_router)

    return application


app = get_application()
