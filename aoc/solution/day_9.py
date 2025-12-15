from io import TextIOWrapper
from typing import Iterator

from aoc.grid import Grid


def part_1(raw_input: TextIOWrapper) -> int:
    tiles = [*parse_tiles(raw_input)]

    return max(
        tile_area(tiles[i], tiles[j])
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )


def part_2(raw_input: TextIOWrapper) -> int:
    tiles = [*parse_tiles(raw_input)]

    # compress coordinates
    comp_x, cols = compress([tile[0] for tile in tiles])
    comp_y, rows = compress([tile[1] for tile in tiles])
    compressed = [*zip(comp_x, comp_y)]

    # populate grid with edges
    grid = Grid.of_size(rows, cols, ".")
    for i in range(len(tiles)):
        j = (i + 1) % len(tiles)
        grid[(compressed[i][1], compressed[i][0])] = "#"
        grid[(compressed[j][1], compressed[j][0])] = "#"
        if compressed[i][0] == compressed[j][0]:
            start_row, stop_row = (
                min(compressed[i][1], compressed[j][1]) + 1,
                max(compressed[i][1], compressed[j][1]),
            )
            for row in range(start_row, stop_row):
                grid[(row, compressed[i][0])] = "X"
        else:
            start_col, stop_col = (
                min(compressed[i][0], compressed[j][0]) + 1,
                max(compressed[i][0], compressed[j][0]),
            )
            for col in range(start_col, stop_col):
                grid[(compressed[i][1], col)] = "X"

    print(grid)

    raise NotImplementedError


def tile_area(t1: tuple[int, int], t2: tuple[int, int]) -> int:
    return abs(t1[0] - t2[0] + 1) * abs(t1[1] - t2[1] + 1)


def parse_tiles(raw_input: TextIOWrapper) -> Iterator[tuple[int, int]]:
    for line in raw_input:
        [x, y] = line.strip().split(",")
        yield int(x), int(y)


def compress(nums: list[int]) -> tuple[list[int], int]:
    """
    Coordinate compression with a twist: successive points will differ by not
    one, but two. This allows convex parts of the polygon to remain.
    """
    val_to_idx = {n: i * 2 for i, n in enumerate(sorted(set(nums)))}
    return [val_to_idx[n] for n in nums], max(val_to_idx.values()) + 1
