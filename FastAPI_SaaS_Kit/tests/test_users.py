import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_update_me(client: AsyncClient, auth_headers):
    resp = await client.patch(
        "/api/v1/users/me", headers=auth_headers, json={"full_name": "Updated Name"}
    )
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_me(client: AsyncClient, auth_headers):
    resp = await client.delete("/api/v1/users/me", headers=auth_headers)
    assert resp.status_code == 204
    # After soft delete, can't access anymore
    resp2 = await client.get("/api/v1/users/me", headers=auth_headers)
    assert resp2.status_code == 401


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    resp = await client.get("/api/v1/users/me")
    assert resp.status_code == 403
