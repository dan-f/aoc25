import importlib
import time
from pathlib import Path
from typing import Any


def run(day: int, part: int, input_dir: Path) -> tuple[Any, float]:
    day_input_path = input_dir.joinpath(f"{day}.txt")
    part_input_path = input_dir.joinpath(f"{day}_{part}.txt")
    if part_input_path.exists():
        input_path = part_input_path
    elif day_input_path.exists():
        input_path = day_input_path
    else:
        raise FileNotFoundError(f"Missing input file for day {day} part {part}")

    solution_mod = importlib.import_module(f"aoc.solution.day_{day}")

    with input_path.open(encoding="utf-8") as f:
        start_time = time.perf_counter()
        if part == 1:
            result = solution_mod.part_1(f)
        else:
            result = solution_mod.part_2(f)
        elapsed_time = time.perf_counter() - start_time

    return result, elapsed_time
