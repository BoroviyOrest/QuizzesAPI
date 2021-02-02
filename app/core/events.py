from typing import Callable

from motor import motor_asyncio
from fastapi import FastAPI

from core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT


def on_startup_handler(app: FastAPI) -> Callable:
    """Creates motor client"""

    async def start_app():
        app.state.mongodb = motor_asyncio.AsyncIOMotorClient(MONGODB_URL,
                                                             maxPoolSize=MAX_CONNECTIONS_COUNT,
                                                             minPoolSize=MIN_CONNECTIONS_COUNT)

    return start_app


def on_shutdown_handler(app: FastAPI) -> Callable:
    """Closes motor client"""

    async def shut_down():
        app.state.mongodb.close()

    return shut_down
