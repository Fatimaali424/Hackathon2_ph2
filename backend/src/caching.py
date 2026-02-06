"""
Caching module for the Todo API.
"""
import json
import redis
import os
from typing import Optional, Any
from datetime import timedelta
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching operations using Redis.
    Falls back to in-memory caching if Redis is not available.
    """

    def __init__(self):
        self.use_redis = os.getenv("USE_REDIS_CACHE", "false").lower() == "true"

        if self.use_redis:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", "6379")),
                    db=0,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                logger.info("Connected to Redis cache successfully")
            except Exception as e:
                logger.warning(f"Could not connect to Redis: {e}. Falling back to in-memory cache.")
                self.use_redis = False

        if not self.use_redis:
            # In-memory cache fallback
            self.cache = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            if self.use_redis:
                cached_value = self.redis_client.get(key)
                if cached_value:
                    return json.loads(cached_value)
            else:
                cached_value = self.cache.get(key)
                if cached_value:
                    # Check if expired
                    value, expiry_time = cached_value
                    if expiry_time is None or expiry_time > __import__('time').time():
                        return value
                    else:
                        # Remove expired entry
                        del self.cache[key]
        except Exception:
            # Silently handle cache errors
            pass

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = 300) -> bool:
        """
        Set a value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for no expiration)

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_redis:
                if ttl is not None:
                    self.redis_client.setex(key, ttl, json.dumps(value))
                else:
                    self.redis_client.set(key, json.dumps(value))
            else:
                expiry_time = __import__('time').time() + ttl if ttl is not None else None
                self.cache[key] = (value, expiry_time)

            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """
        Delete a value from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_redis:
                result = self.redis_client.delete(key)
                return result > 0
            else:
                if key in self.cache:
                    del self.cache[key]
                    return True
                return False
        except Exception:
            return False

    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.

        Args:
            pattern: Pattern to match keys (e.g., "tasks:*")

        Returns:
            Number of keys deleted
        """
        try:
            if self.use_redis:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
                return 0
            else:
                deleted = 0
                keys_to_delete = [key for key in self.cache if pattern.replace('*', '') in key]
                for key in keys_to_delete:
                    if key in self.cache:
                        del self.cache[key]
                        deleted += 1
                return deleted
        except Exception:
            return 0


# Global cache manager instance
cache_manager = CacheManager()


def get_user_tasks_cache_key(user_id: str) -> str:
    """Generate cache key for user tasks."""
    return f"user_tasks:{user_id}"


def get_task_cache_key(task_id: str) -> str:
    """Generate cache key for a specific task."""
    return f"task:{task_id}"