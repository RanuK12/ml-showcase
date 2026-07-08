from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None


@router.get("/me", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserOut)
async def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.email is not None:
        user.email = data.email
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/me", status_code=204)
async def delete_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user.deleted_at = datetime.now(timezone.utc)
    user.is_active = False
    await db.commit()
