from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .enums import Decision, Flag

class InputsSeen(BaseModel):
    historic_cents: Optional[int] = None
    supplier_cents: Optional[int] = None
    human_cents: Optional[int] = None

class AuditEntry(BaseModel):
    event_id: str
    timestamp: int
    item_id: str

    inputs_seen: InputsSeen
    final_price_cents: int
    decision: Decision

    bias_applied_cents: int
    flags: List[Flag] = Field(default_factory=list)
    rules_hash: str = ""