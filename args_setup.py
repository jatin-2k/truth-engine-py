def args_setup(subparsers):
    add_args(subparsers.add_parser("run", help="Run the Donizo engine to process events"))
    add_args(subparsers.add_parser("clean", help="Clean up resources used by the Donizo engine"))
    add_args(subparsers.add_parser("gen", help="Generate sample events for testing"))
    add_args(subparsers.add_parser("replay", help="Replay events and verify final state hash"))

def add_args(subparser):
    subparser.add_argument(
        "--events",
        required=False,
        help="Input events JSONL file",
        default="./resources/events.jsonl"
    )
    subparser.add_argument(
        "--state",
        required=False,
        help="Rules state JSON file",
        default="./resources/rules_state.json"
    )
    subparser.add_argument(
        "--audit",
        required=False,
        help="Audit log JSONL output file",
        default="./resources/audit_log.jsonl"
    )
    subparser.add_argument(
        "--echo",
        required=False,
        help="Echo JSONL output file",
        default="./resources/echo.jsonl"
    )
    subparser.add_argument(
        "--quotes",
        required=False,
        help="Quotes JSONL input file",
        default="./resources/quotes_registry.json"
    )
    subparser.add_argument(
        "--size",
        required=False,
        help="Maximum size of the events mock",
        type=int,
        default=10
    )
    subparser.add_argument(
        "--verify",
        required=False,
        help="File path to verify the final hash against",
        type=str,
        default="./resources/expected_hash.txt"
    )
