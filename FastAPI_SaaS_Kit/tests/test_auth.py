import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "new@example.com", "password": "securepass1", "full_name": "New User"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    payload = {"email": "dup@example.com", "password": "pass1234", "full_name": "Dup"}
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "login@example.com", "password": "mypass123", "full_name": "Login"
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com", "password": "mypass123"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "wrong@example.com", "password": "correct", "full_name": "W"
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com", "password": "incorrect"
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "ref@example.com", "password": "pass1234", "full_name": "R"
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "ref@example.com", "password": "pass1234"
    })
    refresh_token = login_resp.json()["refresh_token"]
    resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_password_reset_request(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "reset@example.com", "password": "pass1234", "full_name": "R"
    })
    resp = await client.post("/api/v1/auth/password-reset", json={"email": "reset@example.com"})
    assert resp.status_code == 204
