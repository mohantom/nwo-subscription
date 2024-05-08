import logging

from fastapi import APIRouter

from app.core.models import Subscription, Action
from app.subscription.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Manage Subscriptions"])


@router.get(
    "/subscription",
    name="Get active subscriptions for a user",
    responses={
        200: {
            "description": "Get active subscriptions",
            "content": {
                "application/json": {
                    "example": {"email": "wtang6@gmail.com", "start_date": "2024-05-07", "industries": ["Consumer"]},
                }
            },
        },
    },
)
def get_subscriptions(id: str = None, email: str = None):
    logger.info(f"Received request for user {id}, email {email}")
    subscription_service = SubscriptionService()
    result = subscription_service.get_subscription(id, email)
    return result


@router.post("/subscription", name="Save Subscription")
def add_subscription(subscription: Subscription):
    subscription_service = SubscriptionService()
    result = subscription_service.handle_subscription(Action.Subscribe, subscription)
    return result


@router.put("/subscription", name="Save Subscription")
def update_subscription(subscription: Subscription):
    subscription_service = SubscriptionService()
    result = subscription_service.handle_subscription(Action.Update, subscription)
    return result


@router.delete("/subscription", name="Save Subscription")
def delete_subscription(id: str):
    subscription_service = SubscriptionService()
    subscription = Subscription(id=id)
    result = subscription_service.handle_subscription(Action.Unsubscribe, subscription)
    return {"data": result}
