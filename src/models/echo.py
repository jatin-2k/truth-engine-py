from typing import Optional
from pydantic import BaseModel

from .enums import EchoEventStatus

class EchoEventModel(BaseModel):
    status: Optional[EchoEventStatus] = None
    created_at_timestamp: Optional[int] = None
    event_id: Optional[str] = None
    timestamp: Optional[int] = None
    item_id: Optional[str] = None
    request_event: Optional[str] = None
    message: Optional[str] = None
    mutable_ctx: Optional[dict] = None
    existing_quote_ctx: Optional[list] = None
    existing_item_state_ctx: Optional[dict] = None
    existing_state_version: Optional[int] = None