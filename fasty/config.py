from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_password: str
    db_user: str

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
