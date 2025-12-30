from abc import abstractmethod
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.dto.facts import Facts

class BaseRule(BaseModel):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Subclasses must implement this property")

    @abstractmethod
    def execute(self, context: "Facts"):
        raise NotImplementedError("Subclasses must implement this method")