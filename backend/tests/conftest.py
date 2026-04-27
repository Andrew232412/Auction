import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


@pytest_asyncio.fixture
async def test_db():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[f"{settings.database_name}_test"]
    yield db
    await client.drop_database(f"{settings.database_name}_test")
    client.close()
