from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DISCERN_ENV: str = "dev"
    AWS_REGION: str = "us-east-1"
    CERTIFICATE_ARN: str
    WEBSERVICE_BASE_URL: str
    USERPOOL_ID: str
    CLIENT_ID: str
    SECRETS_KEY: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
