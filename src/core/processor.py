from src.models.request import PricingRequest
from src.core.config import Config
from src.engine.brain.orchestrator import Orchestrator

class Processor:
    def __init__(self, config: Config) -> None:
        self.orchestrator = Orchestrator(config)
        pass

    def process(self, event_data) -> None:
        pricingEvent = PricingRequest.model_validate(event_data)
        self.orchestrator.execute(pricingEvent)