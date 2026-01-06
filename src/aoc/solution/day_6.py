import re
from enum import Enum
from math import prod
from typing import TextIO

from aocli import solution


@solution(day=6, part=1)
def part_1(raw_input: TextIO) -> int:
    lines = [line.strip() for line in raw_input]
    num_data = lines[:-1]
    op_data = lines[-1]

    operations = [Operation.from_str(o) for o in re.split(r"\s+", op_data)]

    nums = [[int(num) for num in re.split(r"\s+", line)] for line in num_data]
    rows = len(nums)
    cols = len(nums[0])
    nums_flipped = []
    for c in range(cols):
        new_row = []
        for r in range(rows):
            new_row.append(nums[r][c])
        nums_flipped.append(new_row)

    return sum(eval(op, nums) for op, nums in zip(operations, nums_flipped))


@solution(day=6, part=2)
def part_2(raw_input: TextIO) -> int:
    lines = [line.strip("\n") for line in raw_input]
    problem_columns = [
        (Operation.from_str(match.group()[0]), range(*match.span()))
        for match in re.finditer(r"[\+\*]\s*", lines[-1])
    ]

    total = 0

    for operation, col_range in problem_columns:
        nums = []
        for c in col_range:
            digits = []
            for r in range(len(lines) - 1):
                if lines[r][c].isdigit():
                    digits.append(lines[r][c])
            if digits:
                nums.append(int("".join(digits)))
        total += eval(operation, nums)

    return total


class Operation(Enum):
    ADD = "+"
    MUL = "*"

    @classmethod
    def from_str(cls, s: str) -> "Operation":
        match s:
            case "+":
                return Operation.ADD
            case "*":
                return Operation.MUL
            case _:
                raise ValueError(f"Unknown operation: {s}")


def eval(op: Operation, nums: list[int]) -> int:
    match op:
        case Operation.ADD:
            return sum(nums)
        case Operation.MUL:
            return prod(nums)
