import math
from functools import cache
from io import TextIOWrapper
from typing import Generator


def part_1(input: TextIOWrapper) -> int:
    invalid_ids = 0

    for start_str, end_str in parse_ranges(input):
        # ranges containing all odd-lengthed IDs need not be considered
        if len(start_str) == len(end_str) and len(start_str) % 2 == 1:
            continue

        next_invalid = float("-inf")

        for id in range(int(start_str), int(end_str) + 1):
            if id < next_invalid:
                continue

            # skip odd-length IDs
            id_str = str(id)
            if len(id_str) % 2 == 1:
                continue

            front, back = id_str[: len(id_str) // 2], id_str[len(id_str) // 2 :]
            front_i, back_i = int(front), int(back)
            if front_i > back_i:
                next_invalid = int(f"{front}{front}")
            elif front_i < back_i:
                next_invalid = int(f"{(front_i + 1)}{(front_i + 1)}")
            else:
                invalid_ids += id
                next_invalid = int(f"{(front_i + 1)}{(front_i + 1)}")
            if next_invalid > int(end_str):
                break

    return invalid_ids


def part_2(input: TextIOWrapper):
    invalid_ids = 0

    for start_str, end_str in parse_ranges(input):
        if len(start_str) == len(end_str) == 1:
            continue

        for id in range(int(start_str), int(end_str) + 1):
            id_str = str(id)
            for p in prime_factors(len(id_str)):
                group_len = len(id_str) // p
                groups = [
                    id_str[i * group_len : i * group_len + group_len] for i in range(p)
                ]
                if all(g == groups[0] for g in groups):
                    invalid_ids += id
                    break

    return invalid_ids


@cache
def prime_factors(n: int) -> list[int]:
    return [f for f in primes(n) if n % f == 0]


# begins at 2, so index via nums[num - 2]
PRIMES = [True, True]


def primes(limit: int) -> Generator[int]:
    if len(PRIMES) < limit - 1:
        PRIMES.extend(True for _ in range(limit - 1 - len(PRIMES)))
    p = 2
    while p <= int(math.sqrt(limit)):
        if not PRIMES[p - 2]:
            p += 1
            continue
        # yield p
        i = 2
        while (p * i) <= limit:
            PRIMES[p * i - 2] = False
            i += 1
        p += 1

    yield from (i + 2 for i, is_prime in enumerate(PRIMES) if is_prime)


def parse_ranges(input: TextIOWrapper) -> Generator[(str, str)]:
    for range_str in input.read().strip().split(","):
        [start_str, end_str] = range_str.split("-")
        yield start_str, end_str
