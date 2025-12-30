from .base_rule import BaseRule
from src.models.dto.facts import Facts
from src.models.enums import PricingSource, PricingOutcome, Flag, Decision

class RuleB(BaseRule):
    
    @property
    def name(self) -> str:
        return "RuleB"
    
    def execute(self, context: Facts):
        request = context.request_ctx
        state = context.item_state_ctx
        candidate_quote = context.mutable_ctx.candidate.getValue()

        if(request.source == PricingSource.HUMAN and request.outcome == PricingOutcome.QUOTE_ACCEPTED):
            human_price = request.price_cents
            context.mutable_ctx.final_price_cents.adjust(human_price, "RuleB: HUMAN price (Ground Truth)")
            context.mutable_ctx.decision.adjust(Decision.USED_HUMAN, "RuleB: Decision set to USED_HUMAN")
            return
        if(request.source == PricingSource.HUMAN and request.outcome == PricingOutcome.QUOTE_REJECTED):
            context.mutable_ctx.flags.adjust(context.mutable_ctx.flags.getValue() + [Flag.HUMAN_REJECTED], "RuleB: HUMAN quote was rejected")
        
        if(candidate_quote.supplier_quote):
            from_price = context.mutable_ctx.final_price_cents.getValue()
            supplier_price = candidate_quote.supplier_quote.price_cents
            bias = context.mutable_ctx.bias.getValue()
            to_price = supplier_price + bias
            context.mutable_ctx.final_price_cents.adjust(
                to_price,
                f"RuleB: {from_price} -> {to_price} = {supplier_price} + {bias} (SUPPLIER + BIAS)"
            )
            context.mutable_ctx.decision.adjust(
                Decision.USED_SUPPLIER_PLUS_BIAS,
                "RuleB: Decision set to USED_SUPPLIER_PLUS_BIAS"
            )
            return
        
        if(candidate_quote.historic_quote):
            from_price = context.mutable_ctx.final_price_cents.getValue()
            historic_price = candidate_quote.historic_quote.price_cents
            bias = context.mutable_ctx.bias.getValue()
            to_price = historic_price + bias
            context.mutable_ctx.final_price_cents.adjust(
                to_price,
                f"RuleB: {from_price} -> {to_price} = {historic_price} + {bias} (HISTORIC + BIAS)"
            )
            context.mutable_ctx.decision.adjust(
                Decision.USED_HISTORIC_PLUS_BIAS,
                "RuleB: Decision set to USED_HISTORIC_PLUS_BIAS"
            )
            return
        
        context.mutable_ctx.decision.adjust(
            Decision.FALLBACK,
            "RuleB: No valid quotes found, falling back"
        )
