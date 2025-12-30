import argparse
import os
import json
import random
from time import time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from src.core.consumer import stream_events
from src.core.processor import Processor
from src.core.advice import exception_handler
from src.core.config import Config
from args_setup import args_setup

def run(processor: Processor):
    for event in stream_events(Path("./resources/events.jsonl")):
        try :
            processor.process(event)
        except Exception as e:
            exception_handler(e, event)
            print("Processing failed for event:", event.get("event_id"))
            continue

def clean(config: Config, clean_events: bool = True):
    with open(config.audit_log_file_path, "w") as f:
        f.write("")
    with open(config.echo_file_path, "w") as f:
        f.write("")
    with open(config.quotes_file_path, "w") as f:
        f.write("")
    with open(config.rule_state_file_path, "w") as f:
        f.write("")
    with open(config.verification_file_path, "w") as f:
        f.write("")

def gen(config: Config, size: int):
    events = []
    x = 0
    for(item_id) in ["copper_pipe_150mm", "copper_pipe_220mm", "a_steel_pipe_15mm", "a_steel_pipe_22mm", "plastic_pipe_15mm", "plastic_pipe_22mm"]:
        item_events = []
        for i in range(size):
            source = random.choice(["HISTORIC", "HUMAN", "SUPPLIER"])
            timestamp = int(time()) - random.randint(0, 60*60*60*24*30)  # within last 30 days
            item_events.append({
                "readable_ts": datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S %Z"),
                "event_id": f"{x}",
                "item_id": item_id,
                "source": source,
                "price_cents": random.randint(2000,5000) if source == "HUMAN" else random.randint(-100,3000),
                "outcome": random.choice(["QUOTE_ACCEPTED", "QUOTE_REJECTED"] if source == "HUMAN" else ["NONE"]),
                "meta": {"supplier": "point_p"},
                "timestamp": timestamp,
            })
            x += 1
        item_events.sort(key=lambda x: x["timestamp"])
        events.extend(item_events)

    with open(config.events_file_path, "w") as f:
        for event in events:
            f.write(f"{json.dumps(event)}\n")

def verify(config: Config):
    with open(config.rule_state_file_path, "r") as f:
        state_content = f.read()
        state_hash = json.loads(state_content).get("state_hash", None)

    with open(config.verification_file_path, "r") as f:
        expected_hash = f.read().strip()

    if state_hash == expected_hash:
        print("Verification successful: State hash matches expected hash.")
    else:
        print("Verification failed: State hash does not match expected hash.")
        print(f"Computed hash: {state_hash}, Expected hash: {expected_hash}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="donizo_engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    args_setup(subparsers)
    absPath = os.path.dirname(os.path.abspath(__file__))
    args = parser.parse_args()

    config = Config(
        events_file_path=os.path.join(absPath, args.events),
        rule_state_file_path=os.path.join(absPath, args.state),
        audit_log_file_path=os.path.join(absPath, args.audit),
        echo_file_path=os.path.join(absPath, args.echo),
        quotes_file_path=os.path.join(absPath, args.quotes),
        verification_file_path=os.path.join(absPath, args.verify),
    )

    processor = Processor(config)
    
    print("Starting Donizo Engine...")

    if args.command == "run":
        clean(config)
        run(processor)

    if args.command == "clean":
        clean(config)

    if args.command == "gen":
        clean(config)
        gen(config, args.size)

    if args.command == "replay":
        clean(config)
        run(processor)
        verify(config)
