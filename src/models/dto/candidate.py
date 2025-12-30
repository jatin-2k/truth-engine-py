from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from typing import List
from ..enums import PricingSource
from ..quote import QuoteModel

class CandidateQuote(BaseModel):
    supplier_quote: Optional[QuoteModel] = None
    human_quote: Optional[QuoteModel] = None
    historic_quote: Optional[QuoteModel] = None