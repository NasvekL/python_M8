from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.post import PostCreate, PostPatch, PostPut, PostResponse
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    return await post_service.get_posts(db)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await post_service.create_post(db, post)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await post_service.get_post(db, post_id)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post_put(
    post_id: int,
    post_data: PostPut,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await post_service.update_post_put(db, post_id, post_data)


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post_patch(
    post_id: int,
    post_data: PostPatch,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await post_service.update_post_patch(db, post_id, post_data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await post_service.delete_post(db, post_id)
