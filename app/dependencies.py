from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str = "us-east-1"
    ENV: str = "dev"
    CERTIFICATE_ARN: str
    BASE_URL: str
    SECURITY_GROUP_ID: str
    SUBNET_1: str
    SUBNET_2: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
