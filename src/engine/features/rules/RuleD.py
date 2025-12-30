from math import floor
from .base_rule import BaseRule
from src.models.dto.facts import Facts

DECAY_THRESHOLD_SECONDS = 604800  # 7 days in seconds

class RuleD(BaseRule):
    
    @property
    def name(self) -> str:
        return "RuleD"
    
    def execute(self, context: Facts):
        request = context.request_ctx
        state = context.item_state_ctx

        if(state and request.timestamp - state.last_updated_ts > DECAY_THRESHOLD_SECONDS):
            from_bias = context.mutable_ctx.bias.getValue()
            to_bias = floor(from_bias // 2)
            context.mutable_ctx.bias.adjust (
                to_bias,
                f"RuleC: Bias decayed from {from_bias} to {to_bias} due to last update being over 7 days ago"
            )