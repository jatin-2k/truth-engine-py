import json
from pathlib import Path

def stream_events(path: Path):
    with path.open() as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                yield data

            except json.JSONDecodeError as e:
                print(f"[line {line_no}] Invalid JSON: {e}")