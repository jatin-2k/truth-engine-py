#!/usr/bin/env bash
set -e

COMMAND="$1"
shift || true   # remove command from args safely

case "$COMMAND" in
  run|gen|clean|replay)
    make "$COMMAND" ARGS="$*"
    ;;
  *)
    echo "Unknown command: $COMMAND"
    echo "Available commands: run, gen, clean, replay"
    exit 1
    ;;
esac