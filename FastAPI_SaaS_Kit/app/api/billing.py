from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.subscription import Subscription, SubStatus
from app.schemas.subscription import CheckoutRequest
from app.services.stripe_service import (
    create_checkout_session, create_customer,
    create_billing_portal_session, construct_webhook_event,
)

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/checkout")
async def checkout(
    data: CheckoutRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not user.stripe_customer_id:
        user.stripe_customer_id = create_customer(user.email, user.full_name)
        await db.commit()
    url = create_checkout_session(
        user.stripe_customer_id, data.price_id, data.success_url, data.cancel_url
    )
    return {"checkout_url": url}


@router.post("/portal")
async def billing_portal(user: User = Depends(get_current_user)):
    if not user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing account")
    url = create_billing_portal_session(
        user.stripe_customer_id, "http://localhost:3000/billing"
    )
    return {"portal_url": url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = construct_webhook_event(payload, sig)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    obj = event["data"]["object"]

    if event_type == "customer.subscription.created":
        sub = Subscription(
            user_id=obj["metadata"].get("user_id"),
            stripe_subscription_id=obj["id"],
            stripe_price_id=obj["items"]["data"][0]["price"]["id"],
            status=SubStatus.ACTIVE,
        )
        db.add(sub)
        await db.commit()

    elif event_type == "customer.subscription.updated":
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == obj["id"])
        )
        sub = result.scalar_one_or_none()
        if sub:
            status_map = {
                "active": SubStatus.ACTIVE,
                "past_due": SubStatus.PAST_DUE,
                "canceled": SubStatus.CANCELED,
                "trialing": SubStatus.TRIALING,
            }
            sub.status = status_map.get(obj["status"], SubStatus.ACTIVE)
            await db.commit()

    elif event_type == "customer.subscription.deleted":
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == obj["id"])
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubStatus.CANCELED
            await db.commit()

    return {"status": "ok"}
