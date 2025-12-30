from src.models.request import PricingRequest
from src.models.enums import Decision
from src.core.config import Config
from src.core.advice import exception_handler, success_event_handler
from src.engine.brain.helpers.audit_service import AuditManager
from src.engine.brain.helpers.quotes_service import QuotesManager
from src.engine.brain.helpers.state_service import StateManager
from src.engine.features.rulesets.RuleSet1 import RuleSet1
from src.engine.brain.helpers.rule_service import RuleExecutor
from src.engine.brain.utils import Utils
from src.engine.features.utils.TransformerUtils import to_quote

class Orchestrator:
    def __init__(self, config: Config):
        self.stateManager = StateManager(config.rule_state_file_path)
        self.quotesManager = QuotesManager(config.quotes_file_path)
        self.auditManager = AuditManager(config.audit_log_file_path)

    def execute(self, request: PricingRequest):
        ruleSet = RuleSet1()
        facts = Utils.build_facts(request, ruleSet, self.stateManager.get_state(), self.quotesManager.get_quotes(request.item_id))

        for rule in ruleSet.rules:
            RuleExecutor.execute_rule(rule, facts)

        # if(facts.mutable_ctx.decision.getValue() != Decision.FALLBACK):
        self.quotesManager.add_quote(to_quote(request))
        self.stateManager.update_item_state(facts)
        self.auditManager.create_audit_entry(facts)
        success_event_handler(facts)

