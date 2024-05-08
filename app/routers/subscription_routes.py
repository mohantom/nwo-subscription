import logging

from fastapi import APIRouter, Depends
from fastapi import Request

from app.core import auth
from app.core.models import Subscription, Action
from app.subscription.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Manage Subscriptions"])


@router.get(
    "/subscription",
    name="Get active subscriptions for a user",
    responses={
        200: {
            "description": "Win rate by query conditions",
            "content": {
                "application/json": {
                    "example": {"email": "wtang6@gmail.com", "start_date": "2024-05-07T22:52:00", "subscriptions": []},
                }
            },
        },
    },
)
def get_subscriptions(id: str, client: str = Depends(auth.validate_api_key)):
    logger.info(f"Received request from {client} for user {id}")
    subscription_service = SubscriptionService()
    data = subscription_service.get_subscription("")
    return {"data": data}


@router.post("/subscription", name="Save Subscription")
def save_subscription(subscription: Subscription, action: Action):
    subscription_service = SubscriptionService()
    data = subscription_service.save_subscription(action, subscription)
    return {"data": data}
