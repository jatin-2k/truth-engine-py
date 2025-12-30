.PHONY: run clean

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
REQ := requirements.txt

# Marker file to indicate deps are installed
DEPS := $(VENV)/.deps_installed

run: $(DEPS)
	$(PY) -m main run $(ARGS)

# Create venv if missing
$(VENV):
	python3 -m venv $(VENV)

# Install deps only when requirements.txt changes
$(DEPS): $(VENV) $(REQ)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)
	touch $(DEPS)

clean: $(DEPS)
	@if [ -x "$(PY)" ]; then $(PY) -m main clean; fi
	rm -rf $(VENV) .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

gen: $(DEPS)
	$(PY) -m main gen $(ARGS)

replay: $(DEPS)
	$(PY) -m main replay $(ARGS)