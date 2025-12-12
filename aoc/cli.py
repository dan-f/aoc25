from argparse import ArgumentParser


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


parser = ArgumentParser(prog="AoC", description="Advent of Code 2025 solutions")
parser.add_argument("day", type=day)
parser.add_argument("part", type=part)
