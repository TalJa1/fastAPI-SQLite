from httpx import AsyncClient
import pytest
import pytest_asyncio


@pytest.fixture
async def create_customer(async_client: AsyncClient):
    async def _create(body: dict):
        response = await async_client.post("/customers/", json=body)
        return response

    return _create


@pytest_asyncio.fixture
async def test_create_customer(async_client: AsyncClient):
    body = {
        "name": "John Doe",
        "email": "",
        "phone": "1234567890",
    }
    response = await async_client.post("/customers/", json={"body": body})
    assert response.status_code == 201


@pytest_asyncio.fixture
async def test_create_customer_invalid(async_client: AsyncClient):
    body = {
        "name": "John Doe",
        "email": "",
    }
    response = await async_client.post("/customers/", json={"body": body})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "phone"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
