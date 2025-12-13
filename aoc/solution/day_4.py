from io import TextIOWrapper
from typing import Generator, Generic, Iterator, TypeVar

T = TypeVar("T")


class Grid(Generic[T]):
    @staticmethod
    def from_raw(raw_input: TextIOWrapper) -> "Grid[T]":
        return Grid([[c for c in line.strip()] for line in raw_input])

    def __init__(self, data: list[list[T]]):
        self.data = data

    @property
    def rows(self) -> int:
        return len(self.data)

    @property
    def cols(self) -> int:
        return len(self.data[0] if self.data else 0)

    def __getitem__(self, coord: tuple[int, int]) -> list[T]:
        return self.data[coord[0]][coord[1]]

    def __setitem__(self, coord: tuple[int, int], item: T):
        self.data[coord[0]][coord[1]] = item

    def __iter__(self) -> Iterator[tuple[tuple[int, int], T]]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield (r, c), self.data[r][c]

    def __repr__(self):
        items = []
        for (r, c), item in self:
            items.append(repr(item) if type(item) != str else item)
            if r < self.rows - 1 and c == self.cols - 1:
                items.append("\n")
        return "".join(items)


def part_1(raw_input: TextIOWrapper):
    return sum(1 for _ in accessible_rolls(Grid.from_raw(raw_input)))


def part_2(raw_input: TextIOWrapper):
    grid = Grid.from_raw(raw_input)
    removed = 0
    coords = [coord for coord in accessible_rolls(grid)]
    while coords:
        for r, c in coords:
            grid[r, c] = "."
            removed += 1
        coords = [coord for coord in accessible_rolls(grid)]
    return removed


def accessible_rolls(grid: Grid[str]) -> Generator[tuple[int, int]]:
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
