from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from typing import List
from copy import deepcopy

from ..enums import MutableValueType, Decision, Flag
from .candidate import CandidateQuote

T = TypeVar('T')

class MutableValue(BaseModel, Generic[T]):
    type: MutableValueType
    value: T
    ledger: List[str] = Field(default_factory=list)

    def adjust(self, new_value: T, reason: str):
        self.value = new_value
        self.ledger.append(reason)

    def getValue(self) -> T:
        return deepcopy(self.value)
        

class MutableCtx(BaseModel):
    candidate: MutableValue[CandidateQuote] = Field(default_factory=lambda: MutableValue(type=MutableValueType.CANDIDATE, value=CandidateQuote()))
    final_price_cents: MutableValue[int] = Field(default_factory=lambda: MutableValue(type=MutableValueType.FINAL_PRICE_CENTS, value=0))
    decision: MutableValue[Decision] = Field(default_factory=lambda: MutableValue(type=MutableValueType.DECISION, value=Decision.NONE))
    flags: MutableValue[List[Flag]] = Field(default_factory=lambda: MutableValue(type=MutableValueType.FLAG, value=[]))
    bias: MutableValue[int] = Field(default_factory=lambda: MutableValue(type=MutableValueType.BIAS, value=0))
    accepted_human_deltas: MutableValue[List[int]] = Field(default_factory=lambda: MutableValue(type=MutableValueType.FINAL_PRICE_CENTS, value=[]))