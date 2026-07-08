from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, TokenPair, PasswordResetRequest, PasswordResetConfirm
from app.schemas.auth import LoginRequest, RefreshRequest
from app.services.auth_service import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, decode_token, create_password_reset_token,
)
from app.services.email_service import send_welcome_email, send_password_reset_email
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    send_welcome_email(user.email, user.full_name)
    return user


@router.post("/login", response_model=TokenPair)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.email == data.email, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")
    return TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(data: RefreshRequest):
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload["sub"]
    return TokenPair(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/password-reset", status_code=status.HTTP_204_NO_CONTENT)
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if user:
        token = create_password_reset_token(user.email)
        settings = get_settings()
        reset_url = f"{settings.backend_cors_origins[0]}/reset-password?token={token}"
        send_password_reset_email(user.email, reset_url)


@router.post("/password-reset-confirm", status_code=status.HTTP_204_NO_CONTENT)
async def confirm_password_reset(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    payload = decode_token(data.token)
    if not payload or payload.get("type") != "reset":
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    email = payload["sub"]
    result = await db.execute(select(User).where(User.email == email, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = hash_password(data.new_password)
    await db.commit()
