# services/config.py
# services for managing the application configuration

from functools import lru_cache

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    application_env: str
    dbhost: str
    dbname: str
    dbpass: str
    dbuser: str


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
