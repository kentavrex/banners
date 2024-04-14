from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_USER: str = 'default'
    REDIS_PASSWORD: str = ''

    @property
    def REDIS_URL(self):
        redis_address = f'{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'
        return f'redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{redis_address}'


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    TIMEZONE: str = "Europe/Moscow"
    PG_PORT: str = '5432'
    PG_DB: str = 'banners_db'
    PG_USER: str = 'banners_user'
    PG_PASSWORD: str = 'banners_password'
    PG_HOST: str = 'db'
    APP_REDIS_PREFIX: str = ''
    CELERY_BROKER_URL: str = ''
    CELERY_RESULT_BACKEND: str = ''

    @property
    def PG_URL(self) -> str:  # NOQA
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


settings = Settings()
