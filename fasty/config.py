from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_engine: str
    db_host: str
    db_name: str
    db_password: str
    db_user: str
    debug: bool

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
