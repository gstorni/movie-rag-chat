"""
Redis caching service for query results and movie data.
Provides significant speedup for repeated queries.
"""

import redis
import json
import hashlib
from typing import Any, Optional
import sys
sys.path.append('..')
from config import config

# Initialize Redis client
try:
    redis_client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=2
    )
    # Test connection
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("✓ Redis connection established")
except Exception as e:
    print(f"⚠ Redis unavailable: {e}")
    redis_client = None
    REDIS_AVAILABLE = False


def get_query_hash(query: str) -> str:
    """Generate a hash for caching query results."""
    return hashlib.md5(query.encode()).hexdigest()


def cache_get(key: str) -> Optional[Any]:
    """Get cached value and track hit/miss stats."""
    if not REDIS_AVAILABLE:
        return None

    try:
        cached = redis_client.get(key)
        if cached:
            # Increment hit counter
            redis_client.incr("cache:stats:hits")
            return json.loads(cached)
        else:
            # Increment miss counter
            redis_client.incr("cache:stats:misses")
            return None
    except Exception:
        return None


def cache_get_with_status(key: str) -> tuple[Optional[Any], bool]:
    """Get cached value and return (value, was_hit) tuple."""
    if not REDIS_AVAILABLE:
        return None, False

    try:
        cached = redis_client.get(key)
        if cached:
            # Increment hit counter
            redis_client.incr("cache:stats:hits")
            return json.loads(cached), True
        else:
            # Increment miss counter
            redis_client.incr("cache:stats:misses")
            return None, False
    except Exception:
        return None, False


def cache_set(key: str, value: Any, ttl: int = 300):
    """Set cached value with TTL (default 5 minutes)."""
    if not REDIS_AVAILABLE:
        return
    
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass  # Fail silently if Redis is down


def cache_search_results(query: str, results: Any, ttl: int = 300):
    """Cache search results."""
    key = f"search:{get_query_hash(query)}"
    cache_set(key, results, ttl)


def get_cached_search(query: str) -> Optional[Any]:
    """Get cached search results."""
    key = f"search:{get_query_hash(query)}"
    return cache_get(key)


def cache_stats(stats: dict, ttl: int = 3600):
    """Cache database statistics (1 hour TTL)."""
    cache_set("stats:detailed", stats, ttl)


def get_cached_stats() -> Optional[dict]:
    """Get cached statistics."""
    return cache_get("stats:detailed")


def get_redis_stats() -> dict:
    """Get Redis cache statistics."""
    if not REDIS_AVAILABLE:
        return {
            "available": False,
            "status": "disconnected"
        }

    try:
        info = redis_client.info()
        hits = int(redis_client.get("cache:stats:hits") or 0)
        misses = int(redis_client.get("cache:stats:misses") or 0)
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0

        # Count cached items
        search_keys = len(list(redis_client.scan_iter("search:*", count=1000)))
        stats_cached = redis_client.exists("stats:detailed")

        return {
            "available": True,
            "status": "connected",
            "host": f"{config.REDIS_HOST}:{config.REDIS_PORT}",
            "cache_stats": {
                "hits": hits,
                "misses": misses,
                "total_requests": total,
                "hit_rate_percent": round(hit_rate, 2)
            },
            "cached_items": {
                "search_results": search_keys,
                "stats_cached": bool(stats_cached)
            },
            "memory": {
                "used_memory": info.get("used_memory_human", "N/A"),
                "used_memory_peak": info.get("used_memory_peak_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0)
            },
            "server": {
                "version": info.get("redis_version", "N/A"),
                "uptime_days": info.get("uptime_in_days", 0)
            }
        }
    except Exception as e:
        return {
            "available": False,
            "status": "error",
            "error": str(e)
        }


def invalidate_cache():
    """Clear all caches (call when data changes)."""
    if not REDIS_AVAILABLE:
        return

    try:
        # Delete all search and stats keys
        for key in redis_client.scan_iter("search:*"):
            redis_client.delete(key)
        redis_client.delete("stats:detailed")
        print("✓ Cache invalidated")
    except Exception as e:
        print(f"⚠ Cache invalidation failed: {e}")
