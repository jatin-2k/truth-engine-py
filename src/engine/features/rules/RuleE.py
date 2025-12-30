from .base_rule import BaseRule
from src.models.dto.facts import Facts
from src.models.enums import PricingSource, PricingOutcome, Flag, Decision

DECAY_THRESHOLD_SECONDS = 604800  # 7 days in seconds

class RuleE(BaseRule):
    
    @property
    def name(self) -> str:
        return "RuleE"
    
    def execute(self, context: Facts):
        request = context.request_ctx
        state = context.item_state_ctx

        candiate_quote = context.mutable_ctx.candidate.getValue()
        if (candiate_quote.human_quote is None or candiate_quote.supplier_quote is None):
            return
        
        if(candiate_quote.human_quote.price_cents > candiate_quote.supplier_quote.price_cents * 1.5):
            context.mutable_ctx.decision.adjust(
                Decision.FALLBACK,
                "RuleE: human quote being significantly higher than supplier quote"
            )
            context.mutable_ctx.flags.adjust(
                context.mutable_ctx.flags.getValue() + [Flag.ANOMALY_REJECTED],
                "RuleE: Flagged as ANOMALY_REJECTED due to human quote being significantly higher than supplier quote"
            )