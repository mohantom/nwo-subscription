import logging
import uuid
from dataclasses import dataclass
from functools import cached_property

from boto3.dynamodb import conditions

from app.core.boto_handler import BotoHandler
from app.core.constants import ACTIVE_ENDDATE
from app.core.models import Subscription, Action
from app.core.utils import get_all_configs, get_today

logger = logging.getLogger(__name__)


@dataclass
class SubscriptionService:

    def get_subscription(self, email: str) -> Subscription:
        """
        Get user's active subscriptions
        :param email: user's email
        :return: subscrption
        """
        response = self.table.query(
            KeyConditionExpression=conditions.Key("email").eq(email) & conditions.Key("end_date").eq(ACTIVE_ENDDATE)
        )

        subscription = response["Items"][0] if response["Items"] else None
        return subscription

    def save_subscription(self, action: Action, subscription: Subscription):
        """
        Handle user's request for subscribe, unsubscribe and update subscription
        :param subscription: subscription details
        :return:
        """
        if action in [Action.Unsubscribe, Action.Update]:
            self.unsubscribe(subscription)

        if action == Action.Unsubscribe:
            return

        self.subscribe(subscription)
        return

    def unsubscribe(self, subscription: Subscription):
        existing_subscription = self.get_subscription(subscription.id)
        if not existing_subscription:
            logger.info(f"Could not find active subscription for {subscription.id}")
            return

        logger.info("Found existing subscription. Marking it as inactive...")
        expression = "SET end_date = :end_date"
        expression_values = {":end_date": get_today()}
        response = self.table.update_item(
            Key={"id": subscription.id, "end_date": ACTIVE_ENDDATE},
            UpdateExpression=expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW",
        )
        if not response:
            raise Exception("Failed to mark current subscription as inactive.")

        logger.info(f"Successfully unsubscribed for {subscription.email}")

    def subscribe(self, subscription):
        if not subscription.id:
            subscription.id = str(uuid.uuid4())

        logger.info(f"Adding new subscription for {subscription.id}")
        expression = "SET email = :email"
        expression_values = {":email": subscription.email}

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

        response = self.table.update_item(
            Key={"email": subscription.id, "end_date": "2199-12-31"},
            UpdateExpression=expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW",
        )
        logger.info(f"Successfully added subscription for {subscription.email}")
        return response

    @cached_property
    def dynamodb_client(self):
        return BotoHandler.get_resource("dynamodb")

    @cached_property
    def configs(self):
        configs = get_all_configs()
        return configs

    @cached_property
    def table(self):
        table_name = self.configs.get("subscription_table_name", "subscriptions")
        table = self.dynamodb_client.Table(table_name)
        return table
