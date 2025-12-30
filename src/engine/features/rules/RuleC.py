import statistics
from .base_rule import BaseRule
from src.models.dto.facts import Facts
from src.models.enums import PricingSource, PricingOutcome, Flag, Decision

class RuleC(BaseRule):
    
    @property
    def name(self) -> str:
        return "RuleC"
    
    def execute(self, context: Facts):
        request = context.request_ctx
        state = context.item_state_ctx
        candidate_quote = context.mutable_ctx.candidate.getValue()
    
        if(context.mutable_ctx.decision.getValue() == Decision.USED_HUMAN and candidate_quote.supplier_quote):
            human_price = request.price_cents
            supplier_price = candidate_quote.supplier_quote.price_cents
            calculate_delta = human_price - supplier_price
            
            accepted_deltas = [calculate_delta] + context.mutable_ctx.accepted_human_deltas.getValue()
            accepted_deltas = accepted_deltas[:5]

            context.mutable_ctx.accepted_human_deltas.adjust(
                accepted_deltas,
                f"RuleC: Added {calculate_delta} accepted human deltas with latest delta"
            )

            median_delta = int(statistics.median(accepted_deltas))

            context.mutable_ctx.bias.adjust(
                median_delta,
                f"RuleC: Updated bias to median of accepted human deltas: {median_delta}"
            )

