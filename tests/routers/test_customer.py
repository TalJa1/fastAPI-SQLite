from httpx import AsyncClient
import pytest


@pytest.fixture()
async def create_customer(async_client: AsyncClient, body: dict):
    response = await create_customer(async_client, body)
    return response.json()


async def test_create_customer(async_client: AsyncClient):
    body = {
        "name": "John Doe",
        "email": "",
        "phone": "1234567890",
    }
    response = await async_client.post("/customers/", json=body)
    assert response.status_code == 201
