import redis.asyncio as redis
from safir.redis import PydanticRedisStorage
from app.config import settings


r = redis.Redis(port=settings.REDIS_PORT)

def set_storage(datatype) -> PydanticRedisStorage:
    """
    provides storage for saving pydantic models into redis
    datatype pameter is pydantic model class 
    """
    return PydanticRedisStorage(datatype=datatype, redis=r)
     