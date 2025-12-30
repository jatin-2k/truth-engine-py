from time import time

from src.models.echo import EchoEventModel
from src.models.enums import EchoEventStatus
from src.models.dto.facts import Facts

def exception_handler(exc: Exception, event: dict) -> None:
    message = f"An error occurred: {exc}"

    echo_event = EchoEventModel(
        event_id=event.get("event_id"),
        created_at_timestamp=int(time()),
        item_id=event.get("item_id"),
        request_event=str(event),
        status=EchoEventStatus.FAILED,
        message=message
    )

    send_event(echo_event)

def send_event(event: EchoEventModel) -> None:
    with open("./resources/echo.jsonl", "a") as f:
        f.write(event.model_dump_json() + "\n")
    

def success_event_handler(facts: Facts) -> None:
    echo_event = EchoEventModel(
        event_id=facts.request_ctx.event_id,
        created_at_timestamp=int(time()),
        item_id=facts.request_ctx.item_id,
        request_event=str(facts.request_ctx.model_dump()),
        status=EchoEventStatus.SUCCESS,
        message="Event processed successfully",
        mutable_ctx=facts.mutable_ctx.model_dump(),
        existing_quote_ctx=[q.model_dump() for q in facts.quotes_ctx],
        existing_item_state_ctx=facts.item_state_ctx.model_dump() if facts.item_state_ctx else None,
        existing_state_version=facts.state_version
    )

    send_event(echo_event)