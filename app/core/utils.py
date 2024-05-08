import os
from datetime import datetime

from app.core.boto_handler import SecretsManager
from app.dependencies import get_settings


def get_all_configs(env=None) -> dict:
    env = env or os.getenv("env") or os.getenv("ENV") or get_settings().ENV
    secret_id = f"{env}/webservice/config"

    secrets = SecretsManager.extract_secrets(secret_id)
    print(f"Retrieved secrets for {secret_id} from get_all_configs")

    return secrets


def get_today() -> str:
    return datetime.utcnow().isoformat()[:10]
