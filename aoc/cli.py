from argparse import ArgumentParser
from pathlib import Path


def day(s: str) -> int:
    n = int(s)
    if n < 1 or n > 12:
        raise ValueError("Day must be in range [1, 12]")
    return n


def part(s: str) -> int:
    n = int(s)
    if n < 1 or n > 2:
        raise ValueError("Part must be in range [1, 2]")
    return n


def input_dir(s: str) -> Path:
    p = Path(s)
    if not p.exists():
        raise FileNotFoundError(f"Input directory '{p}' does not exist")
    return p


parser = ArgumentParser(prog="AoC", description="Advent of Code 2025 solutions")
subparsers = parser.add_subparsers(dest="command")
parser.add_argument(
    "-i", "--input-dir", type=input_dir, default=Path.cwd().joinpath("input")
)

run_parser = subparsers.add_parser("run", help="run a solution")
run_parser.add_argument("day", type=day)
run_parser.add_argument("part", type=part)

gen_parser = subparsers.add_parser("gen", help="create solution/input files for a day")
gen_parser.add_argument("day", type=day)
