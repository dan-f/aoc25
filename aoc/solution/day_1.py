from io import TextIOWrapper
from typing import Generator


def part_1(input: TextIOWrapper):
    result = 0
    dial = 50
    for turn in rotations(input):
        dial = (dial + turn) % 100
        if dial == 0:
            result += 1
    return result


def part_2(input: TextIOWrapper):
    result = 0
    dial = 50
    for turn in rotations(input):
        total = dial + turn
        if total >= 100:
            result += total // 100
        elif total <= 0:
            result += total // -100
            if dial > 0:
                result += 1
        dial = total % 100
    return result


def rotations(input: TextIOWrapper) -> Generator[int]:
    for line in input:
        line = line.strip()
        num = int(line[1:])
        match line[0]:
            case "R":
                yield num
            case "L":
                yield -num
            case _:
                raise ValueError(f"Unexpected direction: {line[0]}")
