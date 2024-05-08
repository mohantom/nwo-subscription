import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


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
    id: str = str(uuid.uuid4())
    email: str = None
    start_date: str = datetime.utcnow().isoformat()[:10]
    end_date: str = None
    industries: list[Industry] | None = None
    sources: list[Source] | None = None
    subcategories: list[Subcategory] | None = None
