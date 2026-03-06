from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import BASE_DIR
from app.services import post_service

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory=BASE_DIR / "web/templates")


@router.get("/")
@router.get("/posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    db_posts = await post_service.get_posts(db)

    posts_for_template = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "date": post.date_posted.strftime("%Y-%m-%d"),
        }
        for post in db_posts
    ]

    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts_for_template, "title": "Home Page"},
    )


@router.get("/posts/{post_id}", name="read_post")
async def read_post(
    request: Request,
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    post = await post_service.get_post(db, post_id)

    post_for_template = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author.username,
        "user_id": post.user_id,
        "date": post.date_posted.strftime("%Y-%m-%d"),
    }

    return templates.TemplateResponse(
        request,
        "post.html",
        {"post": post_for_template, "title": post.title},
    )
