from fastapi import Request


def init_crud(crud_class) -> callable:
    def wrapper(request: Request):
        return crud_class(request.app.state.mongodb)

    return wrapper
