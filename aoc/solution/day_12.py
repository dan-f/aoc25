from dataclasses import dataclass
from io import TextIOWrapper

from aoc.grid import Grid


def part_1(raw_input: TextIOWrapper) -> int:
    puzzle = parse_input(raw_input)
    print(puzzle)

    """
    What would I do?
    - first check if shape's dimensions can even fit?
    - don't close-off concave sides against a wall
    - place in corners to maximize available room
    - place larger shapes first?
    """

    raise NotImplementedError()


def part_2(raw_input: TextIOWrapper) -> int:
    raise NotImplementedError()


@dataclass
class Region:
    width: int
    length: int
    shapes: list[int]

    @classmethod
    def from_str(cls, s: str) -> Region:
        [dimensions_str, shapes_str] = s.split(": ")
        [width_str, height_str] = dimensions_str.split("x")
        shapes = [int(s) for s in shapes_str.split(" ")]
        return Region(int(width_str), int(height_str), shapes)


@dataclass
class Puzzle:
    regions: list[Region]
    shapes: list[Grid[str]]


def parse_input(raw_input: TextIOWrapper) -> Puzzle:
    [*shapes_blocks, regions_block] = raw_input.read().strip().split("\n\n")
    regions = [Region.from_str(s) for s in regions_block.splitlines()]
    shapes = [Grid.from_lines(iter(block.splitlines()[1:])) for block in shapes_blocks]
    return Puzzle(regions, shapes)
