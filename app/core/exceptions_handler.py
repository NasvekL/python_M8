import logging

from core.config import BASE_DIR
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=BASE_DIR / "web/templates")


def _is_api(request: Request) -> bool:
    return request.url.path.startswith("/api/")


class NotFoundError(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail


class AlreadyExistsError(Exception):
    def __init__(self, detail: str = "Resource already exists"):
        self.detail = detail


async def not_found_handler(request: Request, exc: NotFoundError):
    return await http_exception_handler(
        request,
        StarletteHTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail
        ),
    )


async def already_exists_handler(request: Request, exc: AlreadyExistsError):
    return await http_exception_handler(
        request,
        StarletteHTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    message = exc.detail or "An error occurred"
    if _is_api(request):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "message": message, "title": "Error"},
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if _is_api(request):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Invalid request data", "errors": exc.errors()},
        )
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": "Invalid request data",
            "title": "Validation Error",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    if _is_api(request):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "message": "Internal server error", "title": "Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(AlreadyExistsError, already_exists_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
