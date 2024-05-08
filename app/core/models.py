import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, model_validator


class Action(str, Enum):
    Subscribe = "subscribe"
    Unsubscribe = "unsubscribe"
    Update = "update"


class Industry(str, Enum):
    consumer = "Consumer"
    health = "Health"
    beauty = "Beauty"
    tech = "Tech"


class Source(str, Enum):
    social_media = "Social Media"
    news = "News"


class Subcategory(str, Enum):
    new_product_releases = "New Product Releases"
    mergers = "Mergers"
    acquisitions = "Acquisitions"
    industry = "industry"


class Subscription(BaseModel):
    email: str
    id: str = str(uuid.uuid4())
    start_date: str = datetime.utcnow().isoformat()[:10]
    end_date: str = None
    industries: list[Industry] = None
    sources: list[Source] = None
    subcategories: list[Subcategory] = None

    @model_validator(mode="after")
    def validate_payload(self, values):
        if not self.email:
            raise ValueError("Email is required")

        return values