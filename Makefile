PYTHON := python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
PY     := $(VENV)/bin/python
REQ    := requirements.txt
MAIN   := kanjiscanner.py
SCANS  := scans

.PHONY: help venv install run clean freeze

help:
	@echo "Makefile commands:"
	@echo "  make venv      – create a Python virtual environment in .venv"
	@echo "  make install   – install requirements into .venv"
	@echo "  make run       – run the OCR scanner using the venv"
	@echo "  make clean     – remove all saved scan images"
	@echo "  make freeze    – update requirements.txt from the venv"

venv:
	@echo "Creating virtual environment…"
	$(PYTHON) -m venv $(VENV)

install: venv
	@echo "📦 Installing Python dependencies…"
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)

run:
	$(PY) $(MAIN)

clean:
	@echo "Removing saved scans"
	rm -rf $(SCANS)/*

freeze:
	@echo "Freezing  dependencies"
	$(PIP) freeze > $(REQ)
