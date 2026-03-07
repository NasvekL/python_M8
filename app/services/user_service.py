from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, hash_password, verify_password
from app.core.exceptions_handler import AlreadyExistsError, NotFoundError
from app.models.user import User
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserPatch


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

    return await user_repo.create(
        db,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )


async def patch_user(db: AsyncSession, user_id: int, data: UserPatch):
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    if data.username and data.username.lower() != user.username.lower():
        if await user_repo.get_by_username(db, data.username):
            raise AlreadyExistsError("Username already exists")
        user.username = data.username

    if data.email and data.email.lower() != user.email.lower():
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


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await user_repo.get_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
