import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
from typeguard import typechecked


@typechecked
@pytest.fixture
async def mongodb_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    client.close()


@typechecked
@pytest.mark.asyncio
async def test_mongodb_connection(mongodb_client: AsyncIOMotorClient) -> None:
    db = mongodb_client.test_database
    result = await db.command("ping")
    assert result["ok"] == 1
