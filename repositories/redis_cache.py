import logging
import pickle

from redis import Redis

from config import RedisConfig
from repositories.interfaces import Cache

logger = logging.getLogger(__name__)


class RedisClient(Cache):
    def __init__(self, redis_config: RedisConfig):
        self.db = Redis(
            host=redis_config.REDIS_HOST,
            port=redis_config.REDIS_PORT,
            db=redis_config.REDIS_DB,
            username=redis_config.REDIS_USER,
            password=redis_config.REDIS_PASSWORD,
        )

    def _get(self, key):
        return self.db.get(name=key)

    def _set(self, key, value, *args, **kwargs) -> bool:
        return self.db.set(key, value, *args, **kwargs)

    def _delete(self, *keys):
        return self.db.delete(*keys)

    def _exists(self, *keys):
        return self.db.exists(*keys)

    def get_cached_or_call(self, key: str, expire_time: int):
        def outer(func):
            async def inner(*args, **kwargs):
                if result := self._get(key):
                    logger.info(f"got from cache {key}")
                    return pickle.loads(result)
                result = await func(*args, **kwargs)
                to_cache = pickle.dumps(result)
                self._set(key=key, value=to_cache, ex=expire_time)
                logger.info(f"saved to cache {key}")
                return result

            return inner

        return outer
