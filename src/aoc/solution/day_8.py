import math
from typing import Generic, Hashable, Iterator, TextIO, TypeVar

from aocli import solution


@solution(day=8, part=1)
def part_1(raw_input: TextIO) -> int:
    pairs = closest_pairs([*parse_boxes(raw_input)])
    dj_set = DisjointSet[Coord]()
    i = 0
    for a, b in pairs:
        if i < 1000:
            parent_a, parent_b = dj_set.make_or_find_set(a), dj_set.make_or_find_set(b)
            dj_set.union_sets(parent_a, parent_b)
        else:
            dj_set.make_or_find_set(a)
            dj_set.make_or_find_set(b)
        i += 1

    return math.prod(
        sorted([dj_set.size_of(parent) for parent in dj_set], reverse=True)[:3]
    )


@solution(day=8, part=2)
def part_2(raw_input: TextIO) -> int:
    boxes = [*parse_boxes(raw_input)]
    pairs = closest_pairs(boxes)
    dj_set = DisjointSet[Coord]()
    for a, b in pairs:
        parent_a, parent_b = dj_set.make_or_find_set(a), dj_set.make_or_find_set(b)
        union_parent = dj_set.union_sets(parent_a, parent_b)
        if dj_set.size_of(union_parent) == len(boxes):
            return a[0] * b[0]

    raise RuntimeError("Bug - failed to connect all junction boxes")


Coord = tuple[int, int, int]


def parse_boxes(raw_input: TextIO) -> Iterator[Coord]:
    for line in raw_input:
        nums = line.strip().split(",")
        yield int(nums[0]), int(nums[1]), int(nums[2])


def closest_pairs(boxes: list[Coord]) -> list[tuple[Coord, Coord]]:
    pairs = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            pairs.append((boxes[i], boxes[j]))
    pairs.sort(key=lambda pair: dist(pair[0], pair[1]))
    return pairs


def dist(a: Coord, b: Coord) -> float:
    return math.sqrt(
        math.pow(abs(b[0] - a[0]), 2)
        + math.pow(abs(b[1] - a[1]), 2)
        + math.pow(abs(b[2] - a[2]), 2)
    )


T = TypeVar("T", bound=Hashable)


class DisjointSet(Generic[T]):
    def __init__(self) -> None:
        self.parent: dict[T, T] = {}
        self.size: dict[T, int] = {}

    def make_or_find_set(self, t: T) -> T:
        if t not in self.parent:
            self.parent[t] = t
            self.size[t] = 1
        elif (parent := self.find_set(t)) is not None:
            return parent
        return t

    def find_set(self, t: T) -> T:
        if self.parent[t] == t:
            return t
        return self.find_set(self.parent[t])

    def union_sets(self, a: T, b: T) -> T:
        a_parent, b_parent = self.find_set(a), self.find_set(b)
        if a_parent == b_parent:
            return a_parent
        small, large = (
            (a_parent, b_parent)
            if self.size[a_parent] < self.size[b_parent]
            else (b_parent, a_parent)
        )
        self.parent[small] = large
        self.size[large] += self.size[small]
        del self.size[small]
        return large

    def size_of(self, t: T) -> int:
        return self.size[self.find_set(t)]

    def __iter__(self) -> Iterator[T]:
        yield from (parent for parent in self.size if parent is not None)
