from typing import Callable

from starlette.requests import Request


def get_client(model_class) -> Callable:
    """Get mongoDB client from the request object ind initialize model class with it"""

    def wrapper(request: Request) -> object:
        return model_class(request.app.state.mongodb)

    return wrapper
