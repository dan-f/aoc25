aoc *ARGS:
  uv run main.py {{ARGS}}

check: types ruff

types:
  uv run mypy .

ruff:
  uv run ruff check --fix
  uv run ruff format
