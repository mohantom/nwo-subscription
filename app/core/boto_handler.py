import json
import os

import boto3
import logging

logger = logging.getLogger(__name__)


class BotoHandler:
    __clients = {}

    @classmethod
    def get_resource(cls, resource_name=None):
        if resource_name not in cls.__clients:
            cls.__clients[resource_name] = cls.__connection(resource_name=resource_name, provider=boto3.resource)

        return cls.__clients[resource_name]

    @classmethod
    def get_client(cls, resource_name=None):
        if resource_name not in cls.__clients:
            cls.__clients[resource_name] = cls.__connection(resource_name=resource_name, provider=boto3.client)

        return cls.__clients[resource_name]

    @staticmethod
    def __connection(resource_name=None, provider=None):
        return provider(resource_name, region_name=os.getenv("AWS_REGION"))


class SecretsManager:
    __secrets = {}

    @classmethod
    def extract_secrets(cls, secret_id):
        if secret_id not in cls.__secrets:
            secret_keys = BotoHandler.get_client("secretsmanager").get_secret_value(SecretId=secret_id)
            cls.__secrets[secret_id] = json.loads(secret_keys["SecretString"])

        return cls.__secrets[secret_id]

    @classmethod
    def extract_secrets_no_cache(cls, secret_id):
        secret_keys = BotoHandler.get_client("secretsmanager").get_secret_value(SecretId=secret_id)
        secrets = json.loads(secret_keys["SecretString"])

        return secrets

    @classmethod
    def update_secrets(cls, secret_id, secret_string):
        client = BotoHandler.get_client("secretsmanager")
        response = client.update_secret(SecretId=secret_id, SecretString=secret_string)
        logger.info(response)
        logger.info(f"Updated {secret_id} Value")
        return
