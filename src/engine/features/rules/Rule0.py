from .base_rule import BaseRule
from src.models.dto.facts import Facts
from src.models.enums import PricingSource
from src.models.dto.candidate import CandidateQuote
from src.models.quote import QuoteModel
from ..utils.TransformerUtils import to_quote

class Rule0(BaseRule):
    
    @property
    def name(self) -> str:
        return "Rule0"

    def execute(self, context: Facts):
        state = context.item_state_ctx
        if(state is None):
            return

        context.mutable_ctx.bias.adjust(
            state.bias_cents, 
            "Rule0: Initialize bias with current item bias"
        )
        context.mutable_ctx.accepted_human_deltas.adjust(
            state.accepted_human_deltas_cents,
            "Rule0: Initialize accepted human deltas with current item accepted human deltas"
        )