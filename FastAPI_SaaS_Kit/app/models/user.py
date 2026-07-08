from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(100), default="")
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)
    is_active: Mapped[bool] = mapped_column(default=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(64), default=None)
