from typing import TextIO

from aocli import solution


@solution(day=3, part=1)
def part_1(raw_input: TextIO) -> int:
    joltage = 0
    for line in raw_input:
        line = line.strip()
        first_i, first_c = max(enumerate(line[:-1]), key=lambda x: int(x[1]))
        second_c = max(line[first_i + 1 :], key=int)
        joltage += int(f"{first_c}{second_c}")
    return joltage


@solution(day=3, part=2)
def part_2(raw_input: TextIO) -> int:
    joltage = 0
    for line in raw_input:
        line = line.strip()
        digits = [""] * 12
        start = 0
        end = len(line) - 11
        for d in range(12):
            max_digit = int(line[start])
            max_i = start
            for i in range(start + 1, end):
                digit = int(line[i])
                if digit > max_digit:
                    max_digit = digit
                    max_i = i
            digits[d] = str(max_digit)
            start = max_i + 1
            end = end + 1
        joltage += int("".join(digits))
    return joltage
