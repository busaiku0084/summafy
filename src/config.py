from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mymemory_api_url: str = "https://api.mymemory.translated.net/get"
    translation_timeout: float = 10.0
    log_level: str = "info"

    model_config = {"env_prefix": "SUMMAFY_"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
