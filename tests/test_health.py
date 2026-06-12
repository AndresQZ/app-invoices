import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def health_client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def test_health_returns_ok(health_client):
    async with health_client as client:
        response = await client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
