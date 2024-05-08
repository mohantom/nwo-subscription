import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.boto_handler import BotoHandler


all_api_keys = {}
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def validate_api_key(api_key: str = Security(api_key_header)) -> str:
    # Find company name by api key
    print(f"Validating api key {api_key}")
    if os.getenv("env") == "local":
        return "local"

    if not api_key or (all_api_keys and api_key not in all_api_keys):
        raise HTTPException(status_code=400, detail="x-api-key header invalid")

    if not all_api_keys:
        ag_client = BotoHandler.get_client("apigateway")
        res = ag_client.get_api_keys(includeValues=True)
        for item in res["items"]:
            all_api_keys[item["value"]] = item["name"]

    return all_api_keys[api_key]


def verify_email_address(email: str):
    # TODO
    pass
