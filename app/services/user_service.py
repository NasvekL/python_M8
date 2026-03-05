from core.exceptions_handler import AlreadyExistsError, NotFoundError
from repositories import user_repo
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserPatch


async def get_users(db: AsyncSession):
    return await user_repo.get_all(db)


async def get_user(db: AsyncSession, user_id: int):
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


async def create_user(db: AsyncSession, data: UserCreate):
    if await user_repo.get_by_username(db, data.username):
        raise AlreadyExistsError("Username already exists")
    if await user_repo.get_by_email(db, data.email):
        raise AlreadyExistsError("Email already exists")

    return await user_repo.create(db, username=data.username, email=data.email)


async def patch_user(db: AsyncSession, user_id: int, data: UserPatch):
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    if data.username and data.username != user.username:
        if await user_repo.get_by_username(db, data.username):
            raise AlreadyExistsError("Username already exists")
        user.username = data.username

    if data.email and data.email != user.email:
        if await user_repo.get_by_email(db, data.email):
            raise AlreadyExistsError("Email already exists")
        user.email = data.email

    if data.image_file is not None:
        user.image_file = data.image_file

    return await user_repo.update(db, user)


async def delete_user(db: AsyncSession, user_id: int) -> None:
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    await user_repo.delete(db, user)
