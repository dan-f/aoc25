from io import TextIOWrapper
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Grid(Generic[T]):
    @staticmethod
    def from_raw(raw_input: TextIOWrapper) -> "Grid[str]":
        return Grid([[c for c in line.strip()] for line in raw_input])

    @staticmethod
    def of_size[T](rows: int, cols: int, init: T) -> "Grid[T]":
        return Grid([[init for _ in range(cols)] for _ in range(rows)])

    def __init__(self, data: list[list[T]]):
        self.data = data

    @property
    def rows(self) -> int:
        return len(self.data)

    @property
    def cols(self) -> int:
        return len(self.data[0]) if self.data else 0

    def __getitem__(self, coord: tuple[int, int]) -> T:
        return self.data[coord[0]][coord[1]]

    def __setitem__(self, coord: tuple[int, int], item: T) -> None:
        self.data[coord[0]][coord[1]] = item

    def __contains__(self, coord: tuple[int, int]) -> bool:
        row, col = coord
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __iter__(self) -> Iterator[tuple[tuple[int, int], T]]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield (r, c), self.data[r][c]

    def __repr__(self) -> str:
        items = []
        for (r, c), item in self:
            items.append(repr(item) if type(item) != str else item)
            if r < self.rows - 1 and c == self.cols - 1:
                items.append("\n")
        return "".join(items)
