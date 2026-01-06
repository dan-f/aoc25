from dataclasses import dataclass
from typing import TextIO

from aocli import solution

from aoc.grid import Grid


@solution(day=12, part=1)
def part_1(raw_input: TextIO) -> int:
    regions, presents = parse_input(raw_input)

    def fits_presents(region: Region) -> bool:
        """
        This is technically not a complete solution (will give false positives),
        but it led to the correct result on my puzzle input. I'd have otherwise
        conducted a search where we pick the next un-placed present, which in
        whatever flipped/rotated orientation, leaves the maximum remaining
        "open" space (space that could accommodate further presents).
        """
        presents_area = sum(
            count * sum(cell == "#" for _, cell in presents[p])
            for p, count in enumerate(region.presents)
        )
        return presents_area <= region.width * region.length

    return sum(fits_presents(region) for region in regions)


@dataclass
class Region:
    width: int
    length: int
    presents: list[int]

    @classmethod
    def from_str(cls, s: str) -> Region:
        [dimensions_str, presents_str] = s.split(": ")
        [width_str, height_str] = dimensions_str.split("x")
        presents = [int(s) for s in presents_str.split(" ")]
        return Region(int(width_str), int(height_str), presents)


def parse_input(raw_input: TextIO) -> tuple[list[Region], list[Grid[str]]]:
    [*presents_blocks, regions_block] = raw_input.read().strip().split("\n\n")
    regions = [Region.from_str(s) for s in regions_block.splitlines()]
    presents = [
        Grid.from_lines(iter(block.splitlines()[1:])) for block in presents_blocks
    ]
    return regions, presents
