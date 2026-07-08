import stripe
from app.config import get_settings


def get_stripe():
    settings = get_settings()
    stripe.api_key = settings.stripe_secret_key
    return stripe


def create_checkout_session(customer_id: str, price_id: str, success_url: str, cancel_url: str) -> str:
    s = get_stripe()
    session = s.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url


def create_customer(email: str, name: str) -> str:
    s = get_stripe()
    customer = s.Customer.create(email=email, name=name)
    return customer.id


def create_billing_portal_session(customer_id: str, return_url: str) -> str:
    s = get_stripe()
    session = s.billing_portal.Session.create(customer=customer_id, return_url=return_url)
    return session.url


def construct_webhook_event(payload: bytes, sig_header: str):
    settings = get_settings()
    return stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
