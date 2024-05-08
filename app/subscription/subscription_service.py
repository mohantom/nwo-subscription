import logging
import uuid
from dataclasses import dataclass
from functools import cached_property

from app.core.boto_handler import BotoHandler
from app.core.constants import ACTIVE_ENDDATE
from app.core.models import Subscription, Action
from app.core.utils import get_all_configs, get_today

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:

    def get_subscription(self, id: str) -> Subscription | dict:
        """
        Get user's active subscriptions
        :param id: user id
        :return: subscription
        """
        response = self.table.get_item(Key={"id": id})
        item = response.get("Item")
        if not item:
            return {"message": f"Could not find subscription {id}"}

        subscription = Subscription(**item)
        return subscription

    def handle_subscription(self, action: Action, subscription: Subscription):
        """
        Handle user's request for subscribe, unsubscribe and update subscription
        :param subscription: subscription details
        :return:
        """
        match action:
            case Action.Subscribe:
                return self.save_item(subscription)
            case Action.Update:
                self.archive_item(subscription.id)
                return self.save_item(subscription)
            case Action.Unsubscribe:
                return self.archive_item(subscription.id)
            case _:
                raise ValueError(f"Unsupported action: {action}")

    def archive_item(self, id: str) -> dict:
        existing_subscription = self.get_subscription(id)
        if not existing_subscription:
            message = f"Could not find active subscription for {id}"
            logger.warning(f"Could not find active subscription for {id}")
            return {"message": message}

        logger.info("Found existing subscription. Marking it as inactive...")

        existing_subscription.end_date = get_today()
        self.save_item(existing_subscription, self.table_archive)
        # TODO handle exceptions
        self.table.delete_item(Key={"id": id})

        message = f"Successfully unsubscribed for {id}"
        logger.info(message)
        return {"message": message}

    def save_item(self, subscription: Subscription, table=None) -> dict:
        table = table or self.table
        if not subscription.id:
            subscription.id = str(uuid.uuid4())

        logger.info(f"Adding new subscription for {subscription.id}")
        expression, expression_values = self.create_item_expressions(subscription)

        # TODO handle exceptions
        table.update_item(
            Key={"id": subscription.id},
            UpdateExpression=expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW",
        )

        message = f"Successfully added/updated subscription for {subscription.id}"
        logger.info(message)
        return {"message": message}

    def create_item_expressions(self, subscription) -> tuple[str, dict]:
        expression = "SET email = :email, start_date = :start_date, end_date = :end_date, "
        expression_values = {
            ":email": subscription.email,
            ":start_date": subscription.start_date,
            ":end_date": ACTIVE_ENDDATE,
        }
        if subscription.industries is not None:
            expression += "industries = :industries, "
            expression_values[":industries"] = subscription.industries
        if subscription.sources is not None:
            expression += "sources = :sources, "
            expression_values[":sources"] = subscription.sources
        if subscription.subcategories is not None:
            expression += "subcategories = :subcategories, "
            expression_values[":subcategories"] = subscription.subcategories
        if expression.endswith(", "):
            expression = expression[:-2]
        return expression, expression_values

    @cached_property
    def dynamodb_client(self):
        return BotoHandler.get_resource("dynamodb")

    @cached_property
    def configs(self):
        configs = get_all_configs()
        return configs

    @cached_property
    def table(self):
        table_name = self.configs.get("subscription_table_name", "nwo_subscriptions")
        table = self.dynamodb_client.Table(table_name)
        return table

    @cached_property
    def table_archive(self):
        table_name = self.configs.get("subscription_archive_table_name", "nwo_subscriptions_archive")
        table = self.dynamodb_client.Table(table_name)
        return table
