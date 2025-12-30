from .base_rule import BaseRule
from src.models.dto.facts import Facts
from src.models.enums import PricingSource
from src.models.dto.candidate import CandidateQuote
from src.models.quote import QuoteModel
from ..utils.TransformerUtils import to_quote


SUPPLIER_QUOTE_EXPIRY_SECONDS = 3600  # 1 hour

class RuleA(BaseRule):
    @property
    def name(self) -> str:
        return "RuleA"

    def execute(self, context: Facts):
        request = context.request_ctx
        quotes = context.quotes_ctx
        candidate_quote = context.mutable_ctx.candidate.getValue() or CandidateQuote()

        for quote in quotes:
            if(candidate_quote.supplier_quote is None and quote.source == PricingSource.SUPPLIER and (request.timestamp - quote.timestamp) <= SUPPLIER_QUOTE_EXPIRY_SECONDS):
                candidate_quote.supplier_quote = quote
                context.mutable_ctx.candidate.adjust(candidate_quote, "RuleA: supplier last updated within 1 hour")
            if(candidate_quote.historic_quote is None and quote.source == PricingSource.HISTORIC):
                candidate_quote.historic_quote = quote
                context.mutable_ctx.candidate.adjust(candidate_quote, "RuleA: historical price is present")

        
        if(request.source == PricingSource.HUMAN):
            candidate_quote.human_quote = to_quote(request)
            context.mutable_ctx.candidate.adjust(candidate_quote, "RuleA: Current event source is HUMAN")