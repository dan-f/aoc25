from typing import Iterator, TextIO

from aocli import solution

from aoc.grid import Grid


@solution(day=4, part=1)
def part_1(raw_input: TextIO) -> int:
    return sum(1 for _ in accessible_rolls(Grid.from_lines(raw_input)))


@solution(day=4, part=2)
def part_2(raw_input: TextIO) -> int:
    grid = Grid.from_lines(raw_input)
    removed = 0
    coords = [coord for coord in accessible_rolls(grid)]
    while coords:
        for r, c in coords:
            grid[r, c] = "."
            removed += 1
        coords = [coord for coord in accessible_rolls(grid)]
    return removed


def accessible_rolls(grid: Grid[str]) -> Iterator[tuple[int, int]]:
    for (r, c), item in grid:
        if item != "@":
            continue
        neighbors = (
            grid[r + delta[0], c + delta[1]]
            for delta in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]
            if 0 <= r + delta[0] < grid.rows and 0 <= c + delta[1] < grid.cols
        )
        if len([n for n in neighbors if n == "@"]) < 4:
            yield r, c
