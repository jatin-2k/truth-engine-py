# Donizo Engine

A Python-based event processing engine for managing and analyzing item pricing events.

## Commands

### Using the Shell Script

```bash
./donizo_engine.sh <command> [arguments]
```

Available commands:
- `run` - Process events from the events file
- `gen` - Generate synthetic events
- `clean` - Clean up output files and cache

#### gen
To generate random events for testing

```bash
./donizo_engine.sh gen --size 200
```

Available args:
- `size` - Number of synthetic events to generate per product (default: 10) (products: 6)

#### run
Processes events from the events file.
```bash
./donizo_engine.sh run
```

#### clean
Cleans up all output files, cache, and virtual environment.
```bash
./donizo_engine.sh clean
```

#### replay
Replays events and verifies the state hash. 
Note: Please fill expected hash in `./resources/expected_hash.txt` before running.
```bash
./donizo_engine.sh replay
```


## Setup

The project uses a Python virtual environment for dependency management. The makefile automatically:
1. Creates a `.venv` virtual environment
2. Installs dependencies from `requirements.txt`
3. Manages the installation state with a marker file

## Project Structure

- `main.py` - Main entry point with command handlers
- `makefile` - Build and task automation
- `donizo_engine.sh` - Shell script wrapper for easy command execution
- `src/` - Core source code modules
- `resources/` - Input files and expected outputs for testing
