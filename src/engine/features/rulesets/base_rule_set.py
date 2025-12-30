from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.engine.features.rules.base_rule import BaseRule

class BaseRuleSet(BaseModel):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Subclasses must implement this property")

    @property
    @abstractmethod
    def rules(self) -> list[BaseRule]:
        raise NotImplementedError("Subclasses must implement this method")