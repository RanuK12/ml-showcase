import pytest
from carbonloop.calc import calculate_footprint, factors
from carbonloop.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_calculate_footprint_electricity():
    result = calculate_footprint(electricidad=1000)
    assert result["tCO2e"] > 0
    assert "electricidad" in result["desglose"]


def test_calculate_footprint_all_sources():
    result = calculate_footprint(
        electricidad=1000,
        gas=50,
        combustible=20,
        flota_km=150,
    )
    assert result["tCO2e"] > 0
    assert "scope1" in result["desglose"]
    assert "scope2" in result["desglose"]


def test_negative_inputs():
    with pytest.raises(ValueError):
        calculate_footprint(electricidad=-100)


@pytest.mark.asyncio
async def test_api_footprint():
    response = client.post(
        "/footprint",
        json={
            "electricidad": 1000,
            "gas": 50,
            "combustible": 20,
            "flota_km": 150,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "tCO2e" in data
    assert "desglose" in data


@pytest.mark.asyncio
async def test_api_footprint_pdf():
    response = client.post(
        "/footprint/pdf",
        json={
            "electricidad": 1000,
            "gas": 50,
            "combustible": 20,
            "flota_km": 150,
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
