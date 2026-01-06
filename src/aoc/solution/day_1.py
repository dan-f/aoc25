from typing import Iterator, TextIO

from aocli import solution


@solution(day=1, part=1)
def part_1(raw_input: TextIO) -> int:
    result = 0
    dial = 50
    for turn in rotations(raw_input):
        dial = (dial + turn) % 100
        if dial == 0:
            result += 1
    return result


@solution(day=1, part=2)
def part_2(raw_input: TextIO) -> int:
    result = 0
    dial = 50
    for turn in rotations(raw_input):
        total = dial + turn
        if total >= 100:
            result += total // 100
        elif total <= 0:
            result += total // -100
            if dial > 0:
                result += 1
        dial = total % 100
    return result


def rotations(raw_input: TextIO) -> Iterator[int]:
    for line in raw_input:
        line = line.strip()
        num = int(line[1:])
        match line[0]:
            case "R":
                yield num
            case "L":
                yield -num
            case _:
                raise ValueError(f"Unexpected direction: {line[0]}")
