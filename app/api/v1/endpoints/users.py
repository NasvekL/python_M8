from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.auth import create_access_token, oauth2_scheme, verify_access_token
from app.core.config import settings
from app.schemas.user import Token, UserCreate, UserPatch, UserPrivate, UserPublic
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await user_service.get_users(db)


@router.post("/", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    return await user_service.create_user(db, user)


@router.get("/me", response_model=UserPublic)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get the currently authenticated user based on the provided access token."""
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await user_service.get_user(db, user_id)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await user_service.get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserPrivate)
async def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await user_service.patch_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await user_service.delete_user(db, user_id)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Look up user by email
    # Note: OAuth2PasswordRequestForm has a "username" field, but we are using it to send the email
    user = await user_service.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create and return access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=settings.access_token_expire_delta,
    )
    return Token(access_token=access_token, token_type="bearer")
