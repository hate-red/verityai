import redis.asyncio as redis
from safir.redis import PydanticRedisStorage
from app.config import settings


r = redis.Redis(port=settings.REDIS_PORT)


def get_storage(pydantic_model, prefix = "") -> PydanticRedisStorage:
    """
    Provides storage for saving pydantic models into redis.
    With prefix key in redis looks like this: prefixMyKey.
    """
    return PydanticRedisStorage(datatype=pydantic_model, redis=r, key_prefix=prefix)
    