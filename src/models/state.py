from typing import Optional, List
from pydantic import BaseModel
from hashlib import sha256

class Item(BaseModel):
    bias_cents: int
    last_updated_ts: int
    accepted_human_deltas_cents: List[int]

class State(BaseModel):
    version: int = 1
    items: dict[str, Item] = {}
    state_hash: str = ""

    def set_hash(self):
        state_repr = self.model_dump_json(exclude={"state_hash"})
        self.state_hash = sha256(state_repr.encode('utf-8')).hexdigest()