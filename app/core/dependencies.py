from fastapi import Request


def init_service(service_class) -> callable:
    def wrapper(request: Request):
        return service_class(request.app.state.mongodb)

    return wrapper
