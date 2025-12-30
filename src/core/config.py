from pydantic import BaseModel

class Config(BaseModel):
    events_file_path: str
    rule_state_file_path: str
    audit_log_file_path: str
    echo_file_path: str
    quotes_file_path: str
    verification_file_path: str