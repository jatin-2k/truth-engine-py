from typing import Optional
from pydantic import BaseModel, field_validator, ValidationInfo

from .enums import PricingOutcome, PricingSource

class PricingRequestMeta(BaseModel):
    supplier: str

class PricingRequest(BaseModel):
    event_id: str
    timestamp: int
    item_id: str

    source: PricingSource
    price_cents: int
    outcome: PricingOutcome
    meta: Optional[PricingRequestMeta] = None

    @field_validator("price_cents")
    @classmethod
    def price_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("price_cents must be non-negative")
        return v

    @field_validator("event_id", "item_id", "timestamp", "source", "outcome")
    @classmethod
    def id_must_not_be_empty(cls, v, info: ValidationInfo):
        invalid_fields = []
        if not v:
            invalid_fields.append(info.field_name)
        if invalid_fields:
            raise ValueError(f"{', '.join(invalid_fields)} must not be empty")
        return v