from __future__ import annotations

import time

import redis.asyncio as redis
from fastapi import HTTPException, status

from app.core.config import settings

_redis: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        if not settings.redis_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redis is not configured (REDIS_URL).",
            )
        _redis = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def enforce_rate_limit(*, key: str, limit: int, window_seconds: int) -> None:
    """
    Fixed-window rate limit: increments a counter with TTL.
    Good enough for portfolio/demo; swap to sliding window in real prod.
    """
    r = get_redis()
    now_window = int(time.time()) // window_seconds
    redis_key = f"rl:{key}:{now_window}"

    pipe = r.pipeline()
    pipe.incr(redis_key, 1)
    pipe.expire(redis_key, window_seconds + 5)
    count, _ = await pipe.execute()

    if int(count) > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

