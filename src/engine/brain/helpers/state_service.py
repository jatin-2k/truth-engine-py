from typing import Optional
from time import time
from src.models.dto.facts import Facts
from src.models.state import Item, State

class StateManager:
    def __init__(self, state_file_path: str):
        self.state_file_path = state_file_path

    def get_state(self) -> State:
        state = State()
        state.set_hash()

        with open(self.state_file_path, 'r') as f:
            file_content = f.read()
            if file_content:
                state = State.model_validate_json(file_content)

        return state
    
    def get_item_state(self, item_id: str) -> Optional[Item]:
        state = self.get_state()
        if item_id in state.items:
            return state.items[item_id]
        else:
            return None

    def update_item_state(self, context: Facts) -> None:
        state = self.get_state()
        item_id = context.request_ctx.item_id
        request = context.request_ctx

        new_item : Item = Item(
            bias_cents=context.mutable_ctx.bias.getValue(),
            last_updated_ts=request.timestamp,
            accepted_human_deltas_cents=context.mutable_ctx.accepted_human_deltas.getValue()
        )

        state.version += 1
        state.items[item_id] = new_item
        state.set_hash()

        context.created_rule_state = state

        with open(self.state_file_path, 'w') as f:
            f.write(state.model_dump_json(indent=2))