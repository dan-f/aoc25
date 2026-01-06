from typing import Iterator, TextIO

from aocli import solution

from aoc.grid import Grid


@solution(day=9, part=1)
def part_1(raw_input: TextIO) -> int:
    tiles = [*parse_tiles(raw_input)]

    return max(
        tile_area(tiles[i], tiles[j])
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )


@solution(day=9, part=2)
def part_2(raw_input: TextIO) -> int:
    tiles = [*parse_tiles(raw_input)]
    grid = NormalizedGrid(tiles)

    grid.fill_edges()
    fill_point = grid.find_contained_point()

    if fill_point:
        grid.fill_interior(fill_point)

    return max(
        tile_area(tiles[i], tiles[j])
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if grid.valid_rect(i, j)
    )


def tile_area(t1: tuple[int, int], t2: tuple[int, int]) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def parse_tiles(raw_input: TextIO) -> Iterator[tuple[int, int]]:
    for line in raw_input:
        [x, y] = line.strip().split(",")
        yield int(x), int(y)


class NormalizedGrid:
    def __init__(self, tiles: list[tuple[int, int]]):
        self.tiles = tiles
        comp_x, cols = NormalizedGrid.compress([tile[0] for tile in tiles])
        comp_y, rows = NormalizedGrid.compress([tile[1] for tile in tiles])
        self.compressed = [*zip(comp_x, comp_y)]
        assert len(self.tiles) == len(self.compressed)
        self.grid = Grid.of_size(rows, cols, ".")

    def fill_edges(self) -> None:
        for i in range(len(self.tiles)):
            j = (i + 1) % len(self.tiles)
            self.grid[(self.compressed[i][1], self.compressed[i][0])] = "#"
            self.grid[(self.compressed[j][1], self.compressed[j][0])] = "#"
            if self.compressed[i][0] == self.compressed[j][0]:
                start_row, stop_row = (
                    min(self.compressed[i][1], self.compressed[j][1]) + 1,
                    max(self.compressed[i][1], self.compressed[j][1]),
                )
                for row in range(start_row, stop_row):
                    self.grid[(row, self.compressed[i][0])] = "X"
            else:
                start_col, stop_col = (
                    min(self.compressed[i][0], self.compressed[j][0]) + 1,
                    max(self.compressed[i][0], self.compressed[j][0]),
                )
                for col in range(start_col, stop_col):
                    self.grid[(self.compressed[i][1], col)] = "X"

    def find_contained_point(self) -> tuple[int, int] | None:
        for ray_row in range(self.grid.rows):
            transitions = 0
            prv_tile = self.grid[(ray_row, 0)]
            for ray_col in range(1, self.grid.cols):
                cur_tile = self.grid[(ray_row, ray_col)]
                if prv_tile == "." and (cur_tile == "#" or cur_tile == "X"):
                    transitions += 1
                elif (prv_tile == "#" or prv_tile == "X") and cur_tile == ".":
                    transitions += 1
                prv_tile = cur_tile

                if cur_tile == "." and transitions % 2 == 1:
                    return ray_row, ray_col
        return None

    def fill_interior(self, point: tuple[int, int]) -> None:
        points = [point]
        while points:
            point = points.pop()
            self.grid[point] = "X"
            for row in [-1, 0, 1]:
                for col in [-1, 0, 1]:
                    next_point = (point[0] + row, point[1] + col)
                    if next_point == point:
                        continue
                    if next_point not in self.grid:
                        continue
                    if self.grid[next_point] == "#" or self.grid[next_point] == "X":
                        continue
                    points.append(next_point)

    def valid_rect(self, i: int, j: int) -> bool:
        p1, p2 = self.compressed[i], self.compressed[j]
        first_row, last_row = min(p1[1], p2[1]), max(p1[1], p2[1])
        first_col, last_col = min(p1[0], p2[0]), max(p1[0], p2[0])

        if any(
            self.grid[first_row, col] == "." or self.grid[last_row, col] == "."
            for col in range(first_col, last_col + 1)
        ) or any(
            self.grid[row, first_col] == "." or self.grid[row, first_col] == "."
            for row in range(first_row, last_row + 1)
        ):
            return False

        return True

    @staticmethod
    def compress(nums: list[int]) -> tuple[list[int], int]:
        """
        Coordinate compression with a twist: successive points will differ by not
        one, but two. This allows convex parts of the polygon to remain.
        """
        val_to_idx = {n: i * 2 for i, n in enumerate(sorted(set(nums)))}
        return [val_to_idx[n] for n in nums], max(val_to_idx.values()) + 1
