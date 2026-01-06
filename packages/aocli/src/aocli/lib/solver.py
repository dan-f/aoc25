import time
from typing import Any

from aocli.lib.config import Config
from aocli.lib.day import get_solution

__all__ = ["solve"]


def solve(day: int, part: int, config: Config) -> tuple[Any, float]:
    solution = get_solution(config.solutions_pkg, day, part)

    day_input_path = config.input_dir.joinpath(f"{day}.txt")
    part_input_path = config.input_dir.joinpath(f"{day}_{part}.txt")
    if part_input_path.exists():
        input_path = part_input_path
    elif day_input_path.exists():
        input_path = day_input_path
    else:
        raise FileNotFoundError(f"Missing input file for day {day} part {part}")

    with input_path.open(encoding="utf-8") as f:
        start_time = time.perf_counter()
        result = solution(f)
        elapsed_time = time.perf_counter() - start_time

    return result, elapsed_time
