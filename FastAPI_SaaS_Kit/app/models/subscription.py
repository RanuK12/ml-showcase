import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class SubStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    TRIALING = "trialing"


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    stripe_subscription_id: Mapped[str] = mapped_column(String(64), unique=True)
    stripe_price_id: Mapped[str] = mapped_column(String(64))
    status: Mapped[SubStatus] = mapped_column(default=SubStatus.ACTIVE)
    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
