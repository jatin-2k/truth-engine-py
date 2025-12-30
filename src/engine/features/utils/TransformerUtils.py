from datetime import datetime
from zoneinfo import ZoneInfo
from src.models.request import PricingRequest
from src.models.quote import QuoteModel
from src.models.enums import PricingSource

def to_quote(request: PricingRequest) -> QuoteModel:
    return QuoteModel(
        item_id=request.item_id,
        source=request.source,
        price_cents=request.price_cents,
        outcome=request.outcome,
        timestamp=request.timestamp,
        readable_ts=datetime.fromtimestamp(request.timestamp, tz=ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S %Z"),
        event_id=request.event_id,
    )