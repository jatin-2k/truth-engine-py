from pydantic import BaseModel
from typing import List

from src.models.enums import EchoEventStatus

class RuleExecutionCtx(BaseModel):
    rule_name: str
    executed_at_timestamp: int
    status: EchoEventStatus

class ExecutionCtx(BaseModel):
    rule_set_name: str
    rule_execution_ctx: List[RuleExecutionCtx] = []