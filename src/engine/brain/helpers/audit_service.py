from typing import Optional
from time import time
from src.models.dto.facts import Facts
from src.models.audit import AuditEntry, InputsSeen

class AuditManager:
    def __init__(self, audit_file_path: str):
        self.audit_file_path = audit_file_path

    def create_audit_entry(self, context: Facts) -> None:
        request = context.request_ctx
        mutable_ctx = context.mutable_ctx
        candiate_quote = mutable_ctx.candidate.getValue()
        audit_entry = AuditEntry(
            event_id=request.event_id,
            timestamp=request.timestamp,
            item_id=request.item_id,
            final_price_cents=mutable_ctx.final_price_cents.getValue(),
            decision=mutable_ctx.decision.getValue(),
            bias_applied_cents=mutable_ctx.bias.getValue(),
            flags=mutable_ctx.flags.getValue(),
            rules_hash=context.created_rule_state.state_hash if context.created_rule_state else "",
            inputs_seen=InputsSeen(
                historic_cents=candiate_quote.historic_quote.price_cents if candiate_quote.historic_quote else None,
                supplier_cents=candiate_quote.supplier_quote.price_cents if candiate_quote.supplier_quote else None,
                human_cents=candiate_quote.human_quote.price_cents if candiate_quote.human_quote else None,
            )
        )

        with open(self.audit_file_path, 'a') as f:
            f.write(f"{audit_entry.model_dump_json()}\n")