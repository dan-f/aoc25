aoc *ARGS:
  uv run main.py {{ARGS}}

check: types lint format

types:
  uv run mypy .

lint:
  uv run ruff check

format:
  uv run ruff format
