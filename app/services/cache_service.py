import redis.asyncio as redis
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self, redis_url: str):
        try:
            self.redis = redis.StrictRedis.from_url(redis_url, decode_responses=True)
            logger.info("Redis client created successfully.")
        except Exception as e:
            logger.error(f"Failed to create Redis client: {e}")
            self.redis = None

    async def get(self, key: str) -> Optional[str]:
        if not self.redis:
            logger.error("Redis client is not initialized.")
            return None
        try:
            value = await self.redis.get(key)
            if value:
                logger.info(f"Cache hit for key: {key}")
            else:
                logger.info(f"Cache miss for key: {key}")
            return value
        except Exception as e:
            logger.error(f"Error accessing Redis: {e}")
            return None

    async def set(self, key: str, value: str, expire: int = 3600) -> None:
        if not self.redis:
            logger.error("Redis client is not initialized.")
            return
        try:
            await self.redis.set(key, value, ex=expire)
            logger.info(f"Value set in cache for key: {key}")
        except Exception as e:
            logger.error(f"Error setting value in Redis: {e}")
