from typing import Callable

from fastapi import FastAPI


def on_startup_handler(app: FastAPI) -> Callable:
    """Creates motor client"""

    async def start_app():
        pass

    return start_app


def on_shutdown_handler(app: FastAPI) -> Callable:
    """Closes motor client"""

    async def shut_down():
        pass

    return shut_down
