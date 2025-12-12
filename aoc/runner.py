from typing import Any

import importlib
from os import path


def run(day: int, part: int) -> Any:
    input_dir = path.relpath("input")
    day_input_path = path.join(input_dir, f"{day}.txt")
    part_input_path = path.join(input_dir, f"{day}_{part}.txt")
    if path.exists(part_input_path):
        input_path = part_input_path
    elif path.exists(day_input_path):
        input_path = day_input_path
    else:
        raise FileNotFoundError(f"Missing input file for day {day} part {part}")

    solution_mod = importlib.import_module(f"aoc.solution.day_{day}")

    with open(input_path, "r", encoding="utf-8") as f:
        if part == 1:
            result = solution_mod.part_1(f)
        else:
            result = solution_mod.part_2(f)

    return result
