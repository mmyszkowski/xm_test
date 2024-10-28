import pytest
import pytest_asyncio
from httpx import AsyncClient
from api.api import app


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_order(client):
    response = await client.post("/orders")
    assert response.status_code == 200
    data = response.json()
    assert "orderId" in data
    assert data["status"] == "EXECUTED"


@pytest.mark.asyncio
async def test_get_all_orders(client):
    await client.post("/orders")
    response = await client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_order(client):
    create_response = await client.post("/orders")
    order_id = create_response.json()["orderId"]

    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


@pytest.mark.asyncio
async def test_cancel_order(client):
    create_response = await client.post("/orders")
    order_id = create_response.json()["orderId"]
    response = await client.delete(f"/orders/{order_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_cancel_completed_order(client):
    create_response = await client.post("/orders")
    order_id = create_response.json()["orderId"]
    await client.post("/orders")
    response = await client.delete(f"/orders/{order_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_nonexistent_order(client):
    response = await client.get("/orders/999")
    assert response.status_code == 200
    assert response.json() is None
