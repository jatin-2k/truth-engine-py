from time import time

from src.models.dto.facts import Facts
from src.models.dto.execution_ctx import RuleExecutionCtx
from src.models.enums import EchoEventStatus
from src.models.enums import EchoEventStatus

class RuleExecutor:
    @staticmethod
    def execute_rule(rule, facts: Facts):
        try:
            rule.execute(facts)
            facts.execution_ctx.rule_execution_ctx.append(
                RuleExecutionCtx(
                    rule_name=rule.name,
                    executed_at_timestamp=int(time()),
                    status=EchoEventStatus.SUCCESS,
                )
            )
        except Exception as e:
            facts.execution_ctx.rule_execution_ctx.append(
                RuleExecutionCtx(
                    rule_name=rule.name,
                    executed_at_timestamp=int(time()),
                    status=EchoEventStatus.FAILED,
                )
            )