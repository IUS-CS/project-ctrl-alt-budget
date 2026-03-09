# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python 
PIP = $(VENV)/bin/pip 

# Environment Setup
setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Run Server
run:
	$(PYTHON) run.py
# Testing
test:
	$(PYTHON) -m pytest tests/ -v

# Linting (Need future filenames to work)
lint:
	$(PYTHON) -m pylint app/ run.py

# Data Cleaning
clean:
	rm -rf __pycache__
	rm -rf .venv