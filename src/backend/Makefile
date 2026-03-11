# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python 
PIP = $(VENV)/bin/pip 

# Environment Setup
# Creates virtual environment and installs all dependencies in requirements.txt
# Run once and then activate virtual environment
setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Run Server
# Runs run.py using the venvs python version
run:
	$(PYTHON) run.py
# Testing
test:
	$(PYTHON) -m pytest tests/ -v

# Linting (Need future filenames to work)
lint:
	$(PYTHON) -m pylint app/ run.py

# Data Cleaning
# Deletes all __pycache__ folders, .pytest_cache, and the virtual environment
clean:
	rm -rf __pycache__
	rm -rf .venv