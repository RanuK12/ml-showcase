from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    price_id: str
    success_url: str = "http://localhost:3000/billing/success"
    cancel_url: str = "http://localhost:3000/billing/cancel"


class SubscriptionOut(BaseModel):
    id: str
    status: str
    stripe_price_id: str
    current_period_end: str | None

    model_config = {"from_attributes": True}
