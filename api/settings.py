from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "service-alpha"
    environment: str = "local"
    debug: bool = False
    database_url: str = "postgresql://postgres:postgres@localhost:5432/appdb"
    api_token: str = "dev-token"

    model_config = {"env_prefix": "", "case_sensitive": False}


@lru_cache
def get_settings() -> Settings:
    return Settings()
