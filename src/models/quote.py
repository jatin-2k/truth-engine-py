from typing import Optional, List
from pydantic import BaseModel

from .enums import PricingSource, PricingOutcome

class QuoteModel(BaseModel):
    item_id: str
    source: PricingSource
    price_cents: int
    outcome: PricingOutcome
    timestamp: int
    readable_ts: str
    event_id: str