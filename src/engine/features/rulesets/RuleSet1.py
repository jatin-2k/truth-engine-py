from src.engine.features.rulesets.base_rule_set import BaseRuleSet
from src.engine.features.rules.base_rule import BaseRule
from src.engine.features.rules.Rule0 import Rule0
from src.engine.features.rules.RuleA import RuleA
from src.engine.features.rules.RuleB import RuleB
from src.engine.features.rules.RuleC import RuleC
from src.engine.features.rules.RuleD import RuleD
from src.engine.features.rules.RuleE import RuleE

class RuleSet1(BaseRuleSet):
    @property
    def name(self) -> str:
        return "RuleSet1"

    @property
    def rules(self) -> list[BaseRule]:
        return [
            Rule0(),
            RuleA(),
            RuleB(),
            RuleC(),
            RuleD(),
            RuleE(),
        ]