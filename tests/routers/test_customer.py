from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
# get all customers
async def test_get_customers(async_client: AsyncClient):
    response = await async_client.get("/api/v1/customers")
    assert response.status_code == 200
    assert response.json() == {"customers": []}

    return response.json()
