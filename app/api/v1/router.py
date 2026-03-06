from api.v1.endpoints import health, posts, users
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(posts.router)
