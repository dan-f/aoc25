import importlib
import importlib.util
from pathlib import Path
from typing import Any, Callable, TextIO

from aocli.lib.config import Config
from aocli.lib.input import write_input_file

__all__ = ["solution", "get_solution", "generate_solution"]


SolutionFn = Callable[[TextIO], Any]


solutions: dict[tuple[int, int], SolutionFn] = {}


def solution(day: int, part: int) -> Callable[[SolutionFn], SolutionFn]:
    def decorate(f: SolutionFn) -> SolutionFn:
        if (day, part) in solutions:
            raise RuntimeError(f"Duplicate solution found for day {day} part {part}")
        solutions[day, part] = f
        return f

    return decorate


def get_solution(pkg: str, day: int, part: int) -> SolutionFn:
    importlib.import_module(f".day_{day}", package=pkg)
    try:
        return solutions[day, part]
    except KeyError:
        raise NotImplementedError(f"No solution for day {day} part {part}")


def generate_solution(day: int, config: Config) -> None:
    solutions_dir = (
        (spec := importlib.util.find_spec(config.solutions_pkg))
        and spec
        and spec.origin
        and Path(spec.origin).parent
    )
    if not solutions_dir:
        raise RuntimeError(
            f"Could not find package {config.solutions_pkg}. Ensure __init__.py"
        )

    solution_path = solutions_dir.joinpath(f"day_{day}.py")
    if solution_path.exists():
        raise FileExistsError(f"solution file for day {day} already exists")

    wrote_input, input_path = write_input_file(day, config)
    if wrote_input:
        print(f"Created day {day} input file: {input_path}")
    else:
        print(f"Day {day} input file already exists: {input_path}")

    with solution_path.open("w", encoding="utf-8") as f:
        f.write(solution_template(day))
    print(f"Created day {day} solution file: {solution_path}")


def solution_template(day: int) -> str:
    return f"""from typing import Any, TextIO

from aocli import solution


@solution(day={day}, part={1})
def part_1(raw_input: TextIO) -> Any:
    raise NotImplementedError()


@solution(day={day}, part={2})
def part_2(raw_input: TextIO) -> Any:
    raise NotImplementedError()
"""
