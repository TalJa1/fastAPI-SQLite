import pytest
from httpx import AsyncClient
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from main import app
from routes.CustomerRoute import create_customer


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
