from argparse import ArgumentParser
from pathlib import Path

__all__ = ["parser"]


def part(s: str) -> int:
    n = int(s)
    if n < 1 or n > 2:
        raise ValueError("Part must be in range [1, 2]")
    return n


def path(s: str) -> Path:
    p = Path(s)
    if not p.exists():
        raise FileNotFoundError(f"Path '{p}' does not exist")
    return p


parser = ArgumentParser(prog="AoC", description="Advent of Code 2025 solutions")

subparsers = parser.add_subparsers(dest="command")

solve_parser = subparsers.add_parser("solve", aliases=["s"], help="run a solution")
solve_parser.add_argument("day", type=int)
solve_parser.add_argument("part", type=part)

generate_parser = subparsers.add_parser(
    "generate", aliases=["g"], help="create solution/input files for a day"
)
generate_parser.add_argument("day", type=int)
