from pydantic import BaseModel
from typing import List


from ..request import PricingRequest
from src.models.dto.mutable_ctx import MutableCtx
from src.models.dto.execution_ctx import ExecutionCtx
from src.models.state import Item
from src.models.quote import QuoteModel
from src.models.state import State

class Facts(BaseModel):
    request_ctx: PricingRequest
    item_state_ctx: Item | None = None
    quotes_ctx: List[QuoteModel]
    state_version: int
    execution_ctx: ExecutionCtx
    mutable_ctx: MutableCtx = MutableCtx()
    created_rule_state: State | None = None