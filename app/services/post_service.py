from core.exceptions_handler import NotFoundError
from repositories import post_repo, user_repo
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import PostCreate, PostPatch, PostPut


async def get_posts(db: AsyncSession):
    return await post_repo.get_all(db)


async def get_post(db: AsyncSession, post_id: int):
    post = await post_repo.get_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post not found")
    return post


async def create_post(db: AsyncSession, data: PostCreate):
    user = await user_repo.get_by_id(db, data.user_id)
    if not user:
        raise NotFoundError("User not found")

    return await post_repo.create(
        db,
        title=data.title,
        content=data.content,
        user_id=data.user_id,
    )


async def update_post_put(db: AsyncSession, post_id: int, data: PostPut):
    post = await post_repo.get_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post not found")

    if data.user_id != post.user_id:
        user = await user_repo.get_by_id(db, data.user_id)
        if not user:
            raise NotFoundError("User not found")
        post.user_id = data.user_id

    post.title = data.title
    post.content = data.content

    return await post_repo.update(db, post)


async def update_post_patch(db: AsyncSession, post_id: int, data: PostPatch):
    post = await post_repo.get_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post not found")

    update_data = data.model_dump(exclude_unset=True)

    if "user_id" in update_data and update_data["user_id"] != post.user_id:
        user = await user_repo.get_by_id(db, update_data["user_id"])
        if not user:
            raise NotFoundError("User not found")

    for field, value in update_data.items():
        setattr(post, field, value)

    return await post_repo.update(db, post)


async def delete_post(db: AsyncSession, post_id: int) -> None:
    post = await post_repo.get_by_id(db, post_id)
    if not post:
        raise NotFoundError("Post not found")
    await post_repo.delete(db, post)
