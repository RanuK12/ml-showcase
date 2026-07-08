import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_checkout_no_auth(client: AsyncClient):
    resp = await client.post("/api/v1/billing/checkout", json={"price_id": "price_123"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_portal_no_stripe_customer(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/billing/portal", headers=auth_headers)
    assert resp.status_code == 400
    assert "No billing account" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_webhook_invalid_signature(client: AsyncClient):
    resp = await client.post(
        "/api/v1/billing/webhook",
        content=b'{"type":"test"}',
        headers={"stripe-signature": "invalid"},
    )
    assert resp.status_code == 400
