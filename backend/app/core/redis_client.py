import logging
import time
from typing import Optional, Dict, Tuple
from app.core.config import settings

logger = logging.getLogger("resumeiq.redis")

try:
    import redis
except ImportError:
    redis = None


class ResilientCache:
    """
    Two-tier caching layer:
    1. Uses Redis if reachable.
    2. Gracefully falls back to an in-memory TTL dictionary if Redis is offline or not installed.
    """

    def __init__(self, redis_url: str):
        self.redis_client = None
        self._in_memory_store: Dict[str, Tuple[str, float]] = {}
        self.is_redis_available = False

        if redis:
            try:
                client = redis.from_url(redis_url, socket_connect_timeout=1, socket_timeout=1)
                client.ping()
                self.redis_client = client
                self.is_redis_available = True
                logger.info("Successfully connected to Redis instance.")
            except Exception as e:
                logger.warning(f"Redis not reachable ({e}). Operating in resilient in-memory cache mode.")
                self.is_redis_available = False
        else:
            logger.info("Redis package not installed. Operating in in-memory cache mode.")

    def get(self, key: str) -> Optional[str]:
        if self.is_redis_available and self.redis_client:
            try:
                val = self.redis_client.get(key)
                return val.decode("utf-8") if isinstance(val, bytes) else val
            except Exception as e:
                logger.warning(f"Redis get error ({e}), falling back to memory.")

        # Fallback to in-memory store with TTL check
        item = self._in_memory_store.get(key)
        if item:
            val, expiry = item
            if expiry == 0 or expiry > time.time():
                return val
            else:
                del self._in_memory_store[key]
        return None

    def set(self, key: str, value: str, expire_seconds: int = 3600) -> bool:
        if self.is_redis_available and self.redis_client:
            try:
                self.redis_client.set(key, value, ex=expire_seconds)
                return True
            except Exception as e:
                logger.warning(f"Redis set error ({e}), falling back to memory.")

        expiry = (time.time() + expire_seconds) if expire_seconds > 0 else 0
        self._in_memory_store[key] = (value, expiry)
        return True

    def delete(self, key: str) -> bool:
        if self.is_redis_available and self.redis_client:
            try:
                self.redis_client.delete(key)
                return True
            except Exception:
                pass

        if key in self._in_memory_store:
            del self._in_memory_store[key]
            return True
        return False

    def ping(self) -> bool:
        if self.is_redis_available and self.redis_client:
            try:
                return self.redis_client.ping()
            except Exception:
                return False
        return True


cache = ResilientCache(settings.REDIS_URL)
