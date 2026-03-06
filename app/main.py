from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import BASE_DIR
from app.core.exceptions_handler import register_exception_handlers
from app.web.views import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "web/static"), name="static")
app.mount("/media", StaticFiles(directory=BASE_DIR / "web/media"), name="media")

# Routers
app.include_router(web_router)
app.include_router(api_router)

# Exception handlers
register_exception_handlers(app)
