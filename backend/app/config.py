from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required settings
    JAEGER_FASTAPI_SERVICE: str
    JAEGER_SERVICE_DOMAIN: str

    PG_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


@lru_cache
def get_settings():
    return Settings()

constants = get_settings()