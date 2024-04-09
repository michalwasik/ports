import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from main import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport


@pytest.mark.asyncio
async def test_get_all_routes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/routes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert "route_id" in response.json()[0]


@pytest.mark.asyncio
async def test_get_single_route():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        route_id_expected = 1
        response = await client.get(f"/routes/{route_id_expected}")
        assert response.status_code == 200
        assert "type" in response.json()
        assert response.json()["type"] == "LineString"


@pytest.mark.asyncio
async def test_get_nonexistent_route():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        route_id_nonexistent = 999
        response = await client.get(f"/routes/{route_id_nonexistent}")
        assert response.status_code == 404
