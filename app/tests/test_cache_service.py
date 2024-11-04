import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.services.cache_service import CacheService


@pytest.fixture
def cache_service():
    # Mock the Redis client initialization with a valid URL
    return CacheService(redis_url="redis://localhost:6379")


@pytest.mark.asyncio
async def test_get_value_from_cache(cache_service):
    # Mock the redis get method to return a specific value
    cache_service.redis.get = AsyncMock(return_value="test_value")
    result = await cache_service.get("test_key")
    assert result == "test_value"


@pytest.mark.asyncio
async def test_get_missing_value_from_cache(cache_service):
    # Mock the redis get method to simulate a missing key (None)
    cache_service.redis.get = AsyncMock(return_value=None)
    result = await cache_service.get("missing_key")
    assert result is None


@pytest.mark.asyncio
async def test_set_value_in_cache(cache_service):
    # Mock the redis set method to simulate a successful set operation
    cache_service.redis.set = AsyncMock(return_value=True)
    await cache_service.set("test_key", "test_value", expire=3600)
    cache_service.redis.set.assert_called_once_with("test_key", "test_value", ex=3600)


@pytest.mark.asyncio
async def test_redis_initialization_error():
    with patch("redis.asyncio.StrictRedis.from_url", side_effect=Exception("Initialization error")):
        service = CacheService(redis_url="redis://localhost:6379")
        assert service.redis is None  # Redis client should be None if initialization fails
