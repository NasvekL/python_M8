from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.post import Post


async def get_all(db: AsyncSession) -> list[Post]:
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author))
        .order_by(Post.date_posted.desc())
    )
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(
        select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
    )
    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    title: str,
    content: str,
    user_id: int,
) -> Post:
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    await db.commit()
    return await get_by_id(db, post.id)


async def update(db: AsyncSession, post: Post) -> Post:
    await db.commit()
    return await get_by_id(db, post.id)


async def delete(db: AsyncSession, post: Post) -> None:
    await db.delete(post)
    await db.commit()
