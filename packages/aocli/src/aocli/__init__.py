import sys
from pathlib import Path

from aocli.lib.cli import parser
from aocli.lib.config import load_config
from aocli.lib.day import generate_solution, solution
from aocli.lib.solver import solve

__all__ = ["solution"]


def main() -> None:
    args = parser.parse_args(sys.argv[1:])
    config = load_config(Path.cwd())
    sys.path.append(str(config.source_root))

    match args.command:
        case "solve" | "s":
            result, elapsed_time = solve(args.day, args.part, config)
            print(
                f"Day {args.day} part {args.part} result: {result} (elapsed: {elapsed_time:.3f}s)"
            )
        case "generate" | "g":
            generate_solution(args.day, config)
        case _:
            parser.print_help()
