from collections import deque
from functools import cache
from typing import TextIO

from aocli import solution

from aoc.grid import Grid


@solution(day=7, part=1)
def part_1(raw_input: TextIO) -> int:
    grid = Grid.from_lines(raw_input)
    start_row, start_col = -1, -1
    for (row, col), item in grid:
        if item == "S":
            start_row, start_col = row, col
            break

    splits = 0
    queued = {(start_row + 1, start_col)}
    beams = deque([(start_row + 1, start_col)])
    while beams:
        cur_coord = beams.popleft()
        if cur_coord not in grid:
            continue
        row, col = cur_coord
        next_coord = (row + 1, col)
        if next_coord not in grid:
            continue
        item_below = grid[next_coord]
        if item_below == "^":
            splits += 1
            for coord in [(row + 1, col - 1), (row + 1, col + 1)]:
                if coord in grid and coord not in queued:
                    beams.append(coord)
                    queued.add(coord)
        elif item_below == "." and next_coord not in queued:
            beams.append(next_coord)
            queued.add(next_coord)

    return splits


@solution(day=7, part=2)
def part_2(raw_input: TextIO) -> int:
    grid = Grid.from_lines(raw_input)
    start_row, start_col = -1, -1
    for (row, col), item in grid:
        if item == "S":
            start_row, start_col = row, col
            break

    @cache
    def search(coord: tuple[int, int]) -> int:
        row, col = coord
        if row == grid.rows - 1:
            return 1

        if grid[coord] == "^":
            return search((row + 1, col - 1)) + search((row + 1, col + 1))
        else:
            return search((row + 1, col))

    return search((start_row, start_col))
