from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = "us-east-1"
    ENV: str = "dev"
    CERTIFICATE_ARN: str = None
    BASE_URL: str = None
    SECURITY_GROUP_ID: str = None
    SUBNET_1: str = None
    SUBNET_2: str = None

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
