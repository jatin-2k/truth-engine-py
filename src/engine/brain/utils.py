from typing import List
from src.models.quote import QuoteModel
from src.models.dto.facts import Facts
from src.models.dto.execution_ctx import ExecutionCtx
from src.models.request import PricingRequest
from src.models.state import State, Item
from src.engine.features.rulesets.base_rule_set import BaseRuleSet

class Utils:
    @staticmethod
    def build_facts(request: PricingRequest, ruleSet: BaseRuleSet, state: State, quotes: List[QuoteModel]) -> Facts:
        return Facts(
            request_ctx=request,
            item_state_ctx=state.items.get(request.item_id),
            execution_ctx=ExecutionCtx(
                rule_execution_ctx=[],
                rule_set_name=ruleSet.name
            ),
            state_version=state.version,
            quotes_ctx=quotes
        )