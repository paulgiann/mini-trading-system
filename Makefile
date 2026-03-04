.PHONY: setup test cov run all

setup:
\tpython -m venv .venv || true
\t. .venv/bin/activate && pip install -U pip && pip install -r requirements-dev.txt

test:
\tpytest -q

cov:
\tpytest --cov=. --cov-report=term-missing

run:
\tpython src/main.py

all: test cov run
